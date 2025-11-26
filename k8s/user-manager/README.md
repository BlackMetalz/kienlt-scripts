# 1. Xem các role có sẵn
./k8s-user-manager.sh roles

# 2. Tạo user - chọn role interactively
./k8s-user-manager.sh create kienlt-dev
# Script sẽ show list role và cho bạn chọn số

# 3. Tạo user - chỉ định role trực tiếp
./k8s-user-manager.sh create kienlt-dev viewer-role

# 4. List users
./k8s-user-manager.sh list

# 5. Xem quyền của user
./k8s-user-manager.sh permissions kienlt-dev

# 6. Xóa user
./k8s-user-manager.sh delete kienlt-dev
