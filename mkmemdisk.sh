umount -l "memstore" || true
rm -rf "memstore"
mkdir "memstore"
mount -t tmpfs -o size=400M tmpfs "memstore"
