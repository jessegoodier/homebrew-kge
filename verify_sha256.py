import hashlib
import requests
from urllib.parse import urlparse

packages = {
    "certifi": {
        "url": "https://files.pythonhosted.org/packages/37/f7/2b1b0ec44fdc30a3d31dfebe52226be9ddc40cd6c0f34ffc8923ba423b69/certifi-2022.12.7.tar.gz",
        "expected_sha256": "35824b4c3a97115964b408844d64aa14db1cc518f6562e8d7261699d1350a9e3"
    },
    "charset-normalizer": {
        "url": "https://files.pythonhosted.org/packages/ff/d7/8d757f8bd45be079d76309248845a04f09619a7b17d6dfc8c9ff6433cac2/charset-normalizer-3.1.0.tar.gz",
        "expected_sha256": "34e0a2f9c370eb95597aae63bf85eb5e96826d81e3dcf88b8886012906f509b5"
    },
    "colorama": {
        "url": "https://files.pythonhosted.org/packages/d8/53/6f443c9a4a8358a93a6792e2acffb9d9d5cb0a5cfd8802644b7b1c9a02e4/colorama-0.4.6.tar.gz",
        "expected_sha256": "08695f5cb7ed6e0531a20572697297273c47b8cae5a63ffc6d6ed5c201be6e44"
    },
    "idna": {
        "url": "https://files.pythonhosted.org/packages/8b/e1/43beb3d38dba6cb420cefa297822eac205a277ab43e5ba5d5c46faf96438/idna-3.4.tar.gz",
        "expected_sha256": "814f528e8dead7d329833b91c5faa87d60bf71824cd12a7530b5526063d02cb4"
    },
    "kubernetes": {
        "url": "https://files.pythonhosted.org/packages/b7/e8/0598f0e8b4af37cd9b10d8b87386cf3173cb8045d834ab5f6ec347a758b3/kubernetes-32.0.1.tar.gz",
        "expected_sha256": "42f43d49abd437ada79a79a16bd48a604d3471a117a8347e87db693f2ba0ba28"
    },
    "oauthlib": {
        "url": "https://files.pythonhosted.org/packages/6d/fa/fbf4001037904031639e6bfbfc02badfc7e12f137a8afa254df6c4c8a670/oauthlib-3.2.2.tar.gz",
        "expected_sha256": "9859c40929662bec5d64f34d01c99e093149682a3f38915dc0655d5a633dd918"
    },
    "pyasn1": {
        "url": "https://files.pythonhosted.org/packages/a4/db/fffec68299e6d7bad3d504147f9094830b704527a7fc098b721d38cc7fa7/pyasn1-0.4.8.tar.gz",
        "expected_sha256": "aef77c9fb94a3ac588e87841208bdec464471d9871bd5050a287cc9a475cd0ba"
    },
    "pyasn1-modules": {
        "url": "https://files.pythonhosted.org/packages/88/87/72eb9ccf8a58021c542de2588a867dbefc7556e14b2866d1e40e9e2b587e/pyasn1-modules-0.2.8.tar.gz",
        "expected_sha256": "905f84c712230b2c592c19470d3ca8d552de726050d1d1716282a1f6146be65e"
    },
    "python-dateutil": {
        "url": "https://files.pythonhosted.org/packages/4c/c4/13b4776ea2d76c115c1d1b84579f3764ee6d57204f6be27119f13a61d0a9/python-dateutil-2.8.2.tar.gz",
        "expected_sha256": "0123cacc1627ae19ddf3c27a5de5bd67ee4586fbdd6440d9748f8abb483d3e86"
    },
    "requests": {
        "url": "https://files.pythonhosted.org/packages/9d/ee/391076f5937f0a8cdf5e53b701ffc91753e87b07d66bae4a09aa671897bf/requests-2.28.2.tar.gz",
        "expected_sha256": "98b1b2782e3c6c4904938b84c0eb932721069dfdb9134313beff7c83c2df24bf"
    },
    "requests-oauthlib": {
        "url": "https://files.pythonhosted.org/packages/95/52/531ef197b426646f26b53815a7d2a67cb7a331ef098bb276db26a68ac49f/requests-oauthlib-1.3.1.tar.gz",
        "expected_sha256": "75beac4a47881eeb94d5ea5d6ad31ef88856affe2332b9aafb52c6452ccf0d7a"
    },
    "rsa": {
        "url": "https://files.pythonhosted.org/packages/aa/65/7d973b89c4d2351d7fb232c2e452547ddfa243e93131e7cfa766da627b52/rsa-4.9.tar.gz",
        "expected_sha256": "e38464a49c6c85d7f1351b0126661487a7e0a14a50f1675ec50eb34d4f20ef21"
    },
    "six": {
        "url": "https://files.pythonhosted.org/packages/71/39/171f1c67cd00715f190ba0b100d606d440a28c93c7714febeca8b79af85e/six-1.16.0.tar.gz",
        "expected_sha256": "1e61c37477a1626458e36f7b1d82aa5c9b094fa4802892072e49de9c60c4c926"
    },
    "urllib3": {
        "url": "https://files.pythonhosted.org/packages/c5/52/fe421fb7364aa738b3506a2d99e4f3a56e079c0a798e9f4fa5e14c60922f/urllib3-1.26.14.tar.gz",
        "expected_sha256": "076907bf8fd355cde77728471316625a4d2f7e713c125f51953bb5b3eecf4f72"
    },
    "websocket-client": {
        "url": "https://files.pythonhosted.org/packages/e6/30/fba0d96b4b5fbf5948ed3f4681f7da2f9f64512e1d303f94b4cc174c24a5/websocket_client-1.8.0.tar.gz",
        "expected_sha256": "3239df9f44da632f96012472805d40a23281a991027ce11d2f45a6f24ac4c3da"
    }
}

def verify_sha256(package_name, url, expected_sha256):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        sha256_hash = hashlib.sha256()
        for chunk in response.iter_content(chunk_size=8192):
            sha256_hash.update(chunk)
        
        actual_sha256 = sha256_hash.hexdigest()
        if actual_sha256 == expected_sha256:
            print(f"✅ {package_name}: SHA256 matches")
        else:
            print(f"❌ {package_name}: SHA256 mismatch")
            print(f"  Expected: {expected_sha256}")
            print(f"  Actual:   {actual_sha256}")
    except Exception as e:
        print(f"❌ {package_name}: Error - {str(e)}")

for package_name, data in packages.items():
    verify_sha256(package_name, data["url"], data["expected_sha256"]) 