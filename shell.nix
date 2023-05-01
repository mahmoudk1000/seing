{ pkgs ? import <nixpkgs> {} }:

# let
#   googlesearch = pkgs.python3Packages.mkShell {
#      name = "googlesearch";
#      buildInputs = [
#        pkgs.python3Packages.pip
#        (pkgs.python3Packages.buildPythonPackage {
#          pname = "googlesearch";
#          version = "0.1";
#          src = pkgs.fetchgit {
#            url = "https://github.com/Nv7-GitHub/googlesearch.git";
#            rev = "master";
#          };
#          propagatedBuildInputs = with pkgs.python3Packages; [
#            requests
#            beautifulsoup4
#          ];
#        })
#      ];
#    };
# in

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
    ]))
  ];

  postShellHook = ''
    source ${venvDir}/bin/activate
  '';
}
