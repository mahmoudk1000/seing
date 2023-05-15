{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell rec {
  name = "seing";
  venvDir = "./.venv";

  packages = [
    # googlesearch
    (pkgs.python3.withPackages (ps: [
      ps.flask
      ps.venvShellHook
      ps.flask_sqlalchemy
      ps.flask_login
      ps.werkzeug
      ps.wtforms
      ps.flask_wtf
      ps.beautifulsoup4
      ps.requests
      ps.tld
      ps.tldextract
      ps.urllib3
      ps.fuzzywuzzy
      ps.geoip2
      ps.numpy
      ps.python-Levenshtein
      ps.elasticsearch
    ]))
  ];

  postShellHook = ''
    source ${venvDir}/bin/activate
  '';
}
