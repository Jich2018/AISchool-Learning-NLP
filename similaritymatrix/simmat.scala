val reviews= spark.read.json("dbfs:/FileStore/shared_uploads/weiw@ntdev.microsoft.com/review1.json")
val usermoviereview = reviews.select("asin", "reviewerID", "overall")
val validumr = usermoviereview.filter("overall is NOT null")
val movies = validumr.select(validumr("asin")).distinct
val users = validumr.select(validumr("reviewerID")).distinct

import org.apache.spark.sql.functions._ 
val movieswithid= movies.withColumn("uniqueID",monotonically_increasing_id)
val userswithid = users.withColumn("uniqueID",monotonically_increasing_id)
val ratingswithid= validumr.join(movieswithid, Seq("asin"), "inner").withColumnRenamed("uniqueID", "movieid")
val ratingswithtwoids = ratingswithid.join(userswithid, Seq("reviewerID"), "inner").withColumnRenamed("uniqueID", "userid").withColumnRenamed("overall", "rating").drop("reviewerID").drop("asin")

import org.apache.spark.mllib.linalg.distributed.{CoordinateMatrix, MatrixEntry}
val entries = ratingswithtwoids.map(x  => MatrixEntry(x.getLong(2), x.getLong(1), x.getDouble(0))).rdd
val simmat = new CoordinateMatrix(entries)

simmat.entries.collect