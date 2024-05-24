cmd="use $db;
db.createUser(
  {
      user: "$username",
      pwd: "$password",
      roles: [
          {
              role: "readWrite",
              db: "$db"
          }
      ]
  }
);"

mongo -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD" admin << EOF
$cmd
EOF