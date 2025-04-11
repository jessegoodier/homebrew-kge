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

  def install
    virtualenv_install_with_resources
  end

  test do
    system "#{bin}/kge", "--help"
  end
end
