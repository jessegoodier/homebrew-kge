class Kge < Formula
  include Language::Python::Virtualenv

  desc "Kubernetes utility for viewing pod and failed replicaset events"
  homepage "https://github.com/jessegoodier/kge"
  url "https://files.pythonhosted.org/packages/0f/85/04b881ee4781bfaf6380d67afa37f9f3b593a0af68274aba7b7db09617f0/kge_kubectl_get_events-0.7.11.tar.gz"
  sha256 "c2bc3065f210bbe933b6237962a165fafb168d6167719dcfc15502a7511569cc"
  license "MIT"

  depends_on "python@3.13" => [:build, :test]
  depends_on "poetry-core" => :build

  def install
    # Create virtual environment
    venv = virtualenv_create(libexec, "python3.13")
    
    # Install poetry and its dependencies
    venv.pip_install "poetry-core"
    
    # Install the package using pip directly
    venv.pip_install_and_link buildpath
    # generate_completions_from_executable
  end

  test do
    system bin/"kge", "-v"
  end
end
