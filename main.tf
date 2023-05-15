terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "us-west-2" # Oregon
}

resource "aws_security_group" "app_sg" {
  name        = "app_sg"
  description = "Allow SSH and TCP traffic on port 8080"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "TCP"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "app_server" {
  ami           = "ami-08d70e59c07c61a3a"
  instance_type = "t2.small"
  associate_public_ip_address = true
  key_name         = "id_ed25519"
  vpc_security_group_ids = [aws_security_group.app_sg.id]

  tags = {
    Name = "ObjectDetector"
  }

  root_block_device {
    volume_size = 32
  }
}

resource "aws_key_pair" "ssh-key" {
  key_name   = "id_ed25519"
  public_key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAVlCPR6Uvbz5XxdgfQTat2jZc3gM9mi9FSj7sRDagFQ dimitri@tokyo"
}
