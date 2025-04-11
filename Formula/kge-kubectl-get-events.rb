class KgeKubectlGetEvents < Formula
  include Language::Python::Virtualenv

  desc "A kubernetes utility for viewing pod events in a user-friendly way"
  homepage "https://github.com/jessegoodier/kge"
  url "https://github.com/jessegoodier/kge/raw/refs/heads/main/archive/refs/tags/kge-0.4.0.tar.gz"
  sha256 "3b9a5179c64edb5456d8d6d2252675df07f042710324bd24846f829dc43e9c94"
  license "MIT"

  depends_on "python@3.9"

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