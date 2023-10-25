let
  pkgs = import <nixpkgs> { };

  libraries = with pkgs;[
    webkitgtk
    gtk3
    cairo
    gdk-pixbuf
    glib
    dbus
    openssl_3
  ];

  packages = with pkgs; [
    pkg-config
    dbus
    openssl_3
    glib
    gtk3
    libsoup
    webkitgtk
    appimagekit
  ];
in
pkgs.mkShell {
  buildInputs = packages;

  shellHook =
    ''
      export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath libraries}:$LD_LIBRARY_PATH
    '';
  nativeBuildInputs = [ pkgs.buildPackages.deno
                          pkgs.buildPackages.rustc
                          pkgs.buildPackages.nodejs
                          pkgs.buildPackages.nodejs-21_x
                          pkgs.buildPackages.cargo
                          pkgs.buildPackages.python312
                          # pkgs.buildPackages.nodePackages."@astro"
                          pkgs.buildPackages.bun
                        ];
}