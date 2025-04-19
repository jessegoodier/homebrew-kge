class Kge < Formula
  include Language::Python::Virtualenv

  desc "Kubernetes utility for viewing pod and failed replicaset events"
  homepage "https://pypi.org/project/kge-kubectl-get-events/"
  url "https://files.pythonhosted.org/packages/b9/26/ab3ab6203ea173391a686a301ba9184af5559732dab0ff29c535311f2d93/kge_kubectl_get_events-0.7.0.tar.gz"
  sha256 "4b8d47cb0e1d55eadc06c6f307b8774f4ea25dcff794569527ba42b644a24b85"
  license "MIT"

  depends_on "python@3.11" => :recommended



  resource "colorama" do
    url "https://files.pythonhosted.org/packages/d8/53/6f443c9a4a8358a93a6792e2acffb9d9d5cb0a5cfd8802644b7b1c9a02e4/colorama-0.4.6.tar.gz"
    sha256 "08695f5cb7ed6e0531a20572697297273c47b8cae5a63ffc6d6ed5c201be6e44"
  end


  resource "kubernetes" do
    url "https://pypi.org/packages/source/k/kubernetes/kubernetes-12.0.0.tar.gz"
    sha256 "72f095a1cd593401ff26b3b8d71749340394ca6d8413770ea28ce18efd5bcf4c"
  end
\

  def install
    virtualenv_install_with_resources
  end

  test do
    system bin/"kge", "-v"
  end
end
