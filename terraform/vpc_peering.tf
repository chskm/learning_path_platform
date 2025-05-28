resource "aws_vpc_peering_connection" "ec2_to_aurora" {
  vpc_id      = "vpc-0364ec81cc4a85438" # Replace with EC2 VPC ID
  peer_vpc_id = "vpc-0af7e67ebc573eabf" # Replace with Aurora VPC ID
  auto_accept = true
  tags = {
    Name = "ec2-to-aurora-peering"
  }
}

resource "aws_route" "ec2_to_aurora" {
  route_table_id            = "rtb-0ec721f3a0904cc47" # Replace with EC2 route table ID
  destination_cidr_block    = "10.0.0.0/16" # Replace with Aurora VPC CIDR
  vpc_peering_connection_id = aws_vpc_peering_connection.ec2_to_aurora.id
}

resource "aws_route" "aurora_to_ec2" {
  route_table_id            = "rtb-019f4abc8cb55a780" # Replace with Aurora route table ID
  destination_cidr_block    = "172.31.0.0/16" # Replace with EC2 VPC CIDR
  vpc_peering_connection_id = aws_vpc_peering_connection.ec2_to_aurora.id
}
