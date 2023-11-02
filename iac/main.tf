provider "aws" {
  region  = "us-east-1"
  # You might need to specify other configurations such as access and secret keys.
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


