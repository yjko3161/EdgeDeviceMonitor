-- Database Schema for EdgeDeviceMonitor

-- Create Database (Optional, if not provided by hosting)
CREATE DATABASE IF NOT EXISTS monitor_db;
USE monitor_db;

-- Create Logs Table
CREATE TABLE IF NOT EXISTS logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    host VARCHAR(255),
    status_ping INT,        -- 1: Success, 0: Fail
    status_http INT,        -- 1: Success, 0: Fail
    ping_latency DOUBLE,    -- Seconds
    http_latency DOUBLE,    -- Seconds
    http_status_code INT,
    error_msg TEXT
);
