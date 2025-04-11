class KgeKubectlGetEvents < Formula
  include Language::Python::Virtualenv

  desc "A kubernetes utility for viewing pod events in a user-friendly way"
  homepage "https://github.com/jessegoodier/kge"
  url "https://pypi.org/packages/source/k/kge-kubectl-get-events/kge-kubectl-get-events-0.4.0.tar.gz"
  sha256 "3b9a5179c64edb5456d8d6d2252675df07f042710324bd24846f829dc43e9c94"
  license "MIT"

  depends_on "python@3.9"

  resource "kubernetes" do
    url "https://files.pythonhosted.org/packages/34/19/2f351c0eaf05234dc33a7ba7c3e81b531bc4d3b6b5b1c5a4/kubernetes-12.0.0.tar.gz"
    sha256 "52f1ef257b24f8b3c3c3a3cbf656b4e9f3ebdc187656f1a5e3c461acf8aa774f"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    system "#{bin}/kge", "--help"
  end
end 