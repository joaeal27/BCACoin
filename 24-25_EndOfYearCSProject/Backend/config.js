require("dotenv").config()

const config={
    dbUri:process.env.DB_URI,
    PORT: process.env.PORT
}
module.exports=config;