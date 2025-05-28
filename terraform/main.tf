module "vpc" {
  source     = "./modules/vpc"
  app_name   = var.app_name
  aws_region = var.aws_region
}

module "aurora" {
  source       = "./modules/aurora"
  app_name     = var.app_name
  vpc_id       = module.vpc.vpc_id
  subnet_ids   = module.vpc.private_subnet_ids
  db_username  = var.db_username
  db_password  = var.db_password
}

module "s3_artifacts" {
  source   = "./modules/s3_artifacts"
  app_name = var.app_name
}

module "elastic_beanstalk_backend" {
  source     = "./modules/elastic_beanstalk_backend"
  app_name   = var.app_name
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.public_subnet_ids
  depends_on = [module.s3_artifacts]
}

module "elastic_beanstalk_frontend" {
  source     = "./modules/elastic_beanstalk_frontend"
  app_name   = var.app_name
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.public_subnet_ids
  depends_on = [module.s3_artifacts]
}

module "lambda_api" {
  source             = "./modules/lambda_api"
  app_name           = var.app_name
  vpc_id             = module.vpc.vpc_id
  subnet_ids         = module.vpc.private_subnet_ids
  security_group_ids = [module.vpc.lambda_security_group_id]
}
