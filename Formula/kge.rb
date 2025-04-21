class Kge < Formula
  include Language::Python::Virtualenv

  desc "Kubernetes utility for viewing pod and failed replicaset events"
  homepage "https://github.com/jessegoodier/kge"
  url "https://files.pythonhosted.org/packages/c7/88/429f40057c419d916090ee774145efb53d3a0d67351e45798a0a0f5fb6f5/kge_kubectl_get_events-0.7.8.tar.gz"
  sha256 "3dfcd94ad987b0de62942ff4f60664d16fd7e4c8806786ed15b2f7c90b3e7478"
  license "MIT"

  depends_on "python@3.13" => [:build, :test]
  depends_on "poetry" => :build

  def install
    # Create virtual environment
    venv = virtualenv_create(libexec, "python3.13")
    
    # Install poetry in the virtual environment
    venv.pip_install "poetry"
    
    # Use poetry to install the package and its dependencies
    system "#{libexec}/bin/poetry", "install", "--no-dev", "--no-interaction", "--no-ansi"
    
    # Create symlinks for the executable
    venv.pip_install_and_link buildpath
  end

  test do
    system bin/"kge", "-v"
  end
end
