class Kge < Formula
  include Language::Python::Virtualenv

  desc "Kubernetes utility for viewing pod events in a user-friendly way"
  homepage "https://github.com/jessegoodier/kge"
  url "https://github.com/jessegoodier/kge/raw/refs/heads/main/archive/refs/tags/kge-0.4.1.tar.gz"
  sha256 "0dc2f9c16b5aed58f2a5bdaed7edef337d17e051b8d25c34f0a61bbc3adfc495"
  license "MIT"

  depends_on "python@3.11" => :recommended

  resource "kubernetes" do
    url "https://pypi.org/packages/source/k/kubernetes/kubernetes-12.0.0.tar.gz"
    sha256 "72f095a1cd593401ff26b3b8d71749340394ca6d8413770ea28ce18efd5bcf4c"
  end

  resource "six" do
    url "https://pypi.org/packages/source/s/six/six-1.16.0.tar.gz"
    sha256 "1e61c37477a1626458e36f7b1d82aa5c9b094fa4802892072e49de9c60c4c926"
  end

  resource "python-dateutil" do
    url "https://pypi.org/packages/source/p/python-dateutil/python-dateutil-2.8.2.tar.gz"
    sha256 "0123cacc1627ae1b7437b1357e5a3b58daf9988a89badf1f15ab08d984501125"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    system "#{bin}/kge", "--help"
  end
end
