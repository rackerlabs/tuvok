provider "aws" {
  version = "~> 2.1"
}

provider "aws" {
  alias = "no_version"
}
