with import <nixpkgs> {};
mkShell {
  buildInputs = [
    (python39.withPackages (ps: with ps; [
       pyppeteer
       xlib
       pynput
       rx
       tkinter
    ]))
  ];
  PYTHONPATH="";
  LD_LIBRARY_PATH="";
}
