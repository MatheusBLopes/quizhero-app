provider "aws" {
  region  = "us-east-1"
  # You might need to specify other configurations such as access and secret keys.
}

# Create VPC
resource "aws_vpc" "main" {
  cidr_block           = "172.31.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "MainVpc"
  }
}

# Create Internet Gateway and associate with the VPC
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id
}

# Create a subnet (you can replicate this block for other subnets)
resource "aws_subnet" "subnet_a" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "172.31.32.0/20" # Specify CIDR block for the subnet, e.g., "172.31.1.0/24"
  availability_zone = "us-east-1a" # For other subnets, change this to respective AZs

  tags = {
    Name = "MySubnetA"
  }
}

# Main route table to associate with the VPC
resource "aws_route_table" "main" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = {
    Name = "MainRouteTable"
  }
}

# Associate main route table with the subnet
resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.subnet_a.id
  route_table_id = aws_route_table.main.id
}


resource "aws_security_group" "allow_all" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "allow_all"
  }
}

resource "aws_key_pair" "quizhero_key_pair" {
  key_name   = "quizhero_key_pair"
  public_key = file("./quizhero-key-pair.pub")
}

resource "aws_instance" "quizhero_instance" {
  ami           = "ami-0df435f331839b2d6"
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.subnet_a.id
  vpc_security_group_ids = [aws_security_group.allow_all.id]
  key_name      = aws_key_pair.quizhero_key_pair.key_name

  user_data = <<-EOF
    #!/bin/bash

    # Update the package list
    sudo apt-get update

    # Install Docker
    sudo apt-get install -y docker.io

    # Start Docker and enable it to start on boot
    sudo systemctl start docker
    sudo systemctl enable docker

    # Add the `ubuntu` user to the `docker` group
    sudo usermod -aG docker ec2-user

    # Create a dedicated directory for the app
    sudo mkdir /home/ec2-user/quizhero

    # Set the owner and permissions for the app directory
    sudo chown ec2-user:ec2-user /home/ec2-user/quizhero
    sudo chmod 755 /home/ec2-user/quizhero
  EOF

  tags = {
    Name = "quizhero-instance"
  }
}

resource "aws_eip" "quizhero_ip" {
  instance = aws_instance.quizhero_instance.id
}
