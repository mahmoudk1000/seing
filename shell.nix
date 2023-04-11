#!/usr/bin/env python

{ pkgs ? import <nixpkgs> { } }:

pkgs.mkShell rec {
  name = "seing";
  venvDir = "./.venv";

  packages = [
    (pkgs.python3.withPackages (ps: [
      ps.flask
      ps.venvShellHook
      ps.flask_sqlalchemy
      ps.flask_login
      ps.werkzeug
      ps.wtforms
      ps.flask_wtf
    ]))
  ];

  postShellHook = ''
    source ${venvDir}/bin/activate
  '';
}
