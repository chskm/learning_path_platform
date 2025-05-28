resource "aws_elastic_beanstalk_application" "app" {
  name = "${var.app_name}-frontend"
}

resource "aws_elastic_beanstalk_environment" "env" {
  application         = aws_elastic_beanstalk_application.app.name
  name                = "${var.app_name}-frontend-env"
  solution_stack_name = "64bit Amazon Linux 2023 v4.5.2 running Python 3.11"
  wait_for_ready_timeout = "20m"

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "InstanceType"
    value     = "t3.micro"
  }

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "IamInstanceProfile"
    value     = aws_iam_instance_profile.eb_profile.name
  }

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "SecurityGroups"
    value     = aws_security_group.eb_sg.id
  }

  setting {
    namespace = "aws:ec2:vpc"
    name      = "VPCId"
    value     = var.vpc_id
  }

  setting {
    namespace = "aws:ec2:vpc"
    name      = "Subnets"
    value     = join(",", var.subnet_ids)
  }

  setting {
    namespace = "aws:elasticbeanstalk:environment:process:default"
    name      = "Port"
    value     = "8501"
  }

  depends_on = [
    aws_iam_role_policy_attachment.eb_web_policy,
    aws_iam_role_policy_attachment.eb_s3_policy
  ]
}

resource "aws_security_group" "eb_sg" {
  vpc_id = var.vpc_id
  name   = "${var.app_name}-eb-frontend-sg"
  ingress {
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "${var.app_name}-eb-frontend-sg"
  }
}

resource "aws_iam_role" "eb_role" {
  name = "${var.app_name}-eb-frontend-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "eb_web_policy" {
  role       = aws_iam_role.eb_role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSElasticBeanstalkWebTier"
}

resource "aws_iam_role_policy_attachment" "eb_s3_policy" {
  role       = aws_iam_role.eb_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_instance_profile" "eb_profile" {
  name = "${var.app_name}-eb-frontend-profile"
  role = aws_iam_role.eb_role.name
}
