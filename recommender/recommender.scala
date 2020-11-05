val reviews= spark.read.json("dbfs:/FileStore/shared_uploads/weiw@ntdev.microsoft.com/review1.json")
val usermoviereview = reviews.select("asin", "reviewerID", "overall")

//remove rows with empty rating
val validumr = usermoviereview.filter("overall is NOT null")

//get unique movies and users
val movies = validumr.select(validumr("asin")).distinct
val users = validumr.select(validumr("reviewerID")).distinct

//add id column using row number
movies.createOrReplaceTempView("movies")
val moviesid = spark.sql("""select row_number() over (order by "asin") as id, * from movies""")
users.createOrReplaceTempView("users")
val usersid = spark.sql("""select row_number() over (order by "reviewerID") as id, * from users""")
val ratingswithid= validumr.join(moviesid, Seq("asin"), "inner").withColumnRenamed("id", "movieid").drop("asin")

//now ratingswithtwoids have 3 columns: rating, movieid, userid
val ratingswithtwoids = ratingswithid.join(usersid, Seq("reviewerID"), "inner").withColumnRenamed("id", "userid").withColumnRenamed("overall", "rating").drop("reviewerID")

import org.apache.spark.ml.evaluation.RegressionEvaluator
import org.apache.spark.ml.recommendation.ALS


val Array(training, test) = ratingswithtwoids.randomSplit(Array(0.8, 0.2))

// Build the recommendation model using ALS on the training data
val als = new ALS()
  .setMaxIter(100)
  .setRegParam(0.01)
  .setRank(20)
  .setUserCol("userid")
  .setItemCol("movieid")
  .setRatingCol("rating")
val model = als.fit(training)

// Evaluate the model by computing the RMSE on the test data
val predictions = model.transform(test)

val evaluator = new RegressionEvaluator()
  .setMetricName("rmse")
  .setLabelCol("rating")
  .setPredictionCol("prediction")
val rmse = evaluator.evaluate(predictions.na.drop())
println(s"Root-mean-square error = $rmse")

val top3recommendations = model.recommendForAllUsers(3)
top3recommendations.show(20, false)

//upload and save the model and intermediate files
model.save("dbfs:/FileStore/shared_uploads/weiw@ntdev.microsoft.com/alsreview.model")
usersid.coalesce(1).write.format("com.databricks.spark.csv")
  .mode("overwrite")
  .option("header", "true")
  .option("delimiter", ",")
  .option("quoteMode", "true")
  .save("dbfs:/FileStore/shared_uploads/weiw@ntdev.microsoft.com/usersid")
moviesid.coalesce(1).write.format("com.databricks.spark.csv")
  .mode("overwrite")
  .option("header", "true")
  .option("delimiter", ",")
  .option("quoteMode", "true")
  .save("dbfs:/FileStore/shared_uploads/weiw@ntdev.microsoft.com/moviesid")
