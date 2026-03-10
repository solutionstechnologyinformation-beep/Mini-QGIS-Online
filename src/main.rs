use actix_web::{web, App, HttpServer, HttpResponse};
use std::env;

async fn index() -> HttpResponse {
    let html = include_str!("../static/index.html");
    HttpResponse::Ok()
        .content_type("text/html; charset=utf-8")
        .body(html)
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let port = env::var("PORT")
        .unwrap_or_else(|_| "8000".to_string())
        .parse::<u16>()
        .unwrap_or(8000);

    println!("Iniciando servidor na porta {}", port);

    HttpServer::new(|| {
        App::new()
            .route("/", web::get().to(index))
    })
    .bind(("0.0.0.0", port))?
    .run()
    .await
}