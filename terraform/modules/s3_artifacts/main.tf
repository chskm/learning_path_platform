resource "aws_s3_bucket" "artifacts" {
  bucket = "${var.app_name}-artifacts"
  tags = {
    Name = "${var.app_name}-artifacts"
  }
}

resource "aws_s3_bucket_policy" "artifacts_policy" {
  bucket = aws_s3_bucket.artifacts.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = {
          Service = "elasticbeanstalk.amazonaws.com"
        }
        Action    = ["s3:GetObject", "s3:PutObject", "s3:ListBucket"]
        Resource  = [
          aws_s3_bucket.artifacts.arn,
          "${aws_s3_bucket.artifacts.arn}/*"
        ]
      }
    ]
  })
}
