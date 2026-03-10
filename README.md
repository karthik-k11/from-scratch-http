# From-Scratch HTTP Server with MiniDB

A minimal HTTP/1.1 server implemented **from raw TCP sockets in Python**, with a custom request parser, routing system, middleware pipeline, logging, threaded concurrency, and a network-accessible key-value database.

This project demonstrates **backend systems fundamentals** by building core web server components without using frameworks like Flask, FastAPI, or Django.

---

## Features

- Raw TCP socket server
- Custom HTTP/1.1 request parsing
- Routing system (`method + path`)
- Query parameter parsing
- POST request support
- JSON body parsing
- Thread-per-connection concurrency model
- Middleware pipeline
- Structured logging
- Simple in-memory key-value database (MiniDB)
- Benchmarking tool for load testing

---

## Architecture
``` bash 
Clients
↓
TCP Socket Server
↓
Thread-per-connection
↓
HTTP Parser
↓
Middleware Pipeline
↓
Router
↓
Handlers
↓
MiniDB (Key-Value Store)
↓
Logging
```
