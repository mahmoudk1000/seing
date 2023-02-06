#!/usr/bin/env python

{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell rec {
  name = "seing";
  venvDir = "./.venv";

  packages = [
    (pkgs.python3.withPackages (ps: [
      ps.flask
      ps.venvShellHook
      ps.pytest
    ]))
  ];

  postShellHook = ''
    source ${venvDir}/bin/activate
  '';
}
