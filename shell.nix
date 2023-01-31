
{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = [
    # here goes python pkgs
    (pkgs.python3.withPackages (ps: [
      ps.flask
    ]))
    # here goes normael pkgs
  ];
}