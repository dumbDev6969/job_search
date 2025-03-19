CREATE TABLE IF NOT EXISTS password_reset_tokens (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    token VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    used BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE KEY unique_active_token (email, token),
    INDEX idx_token (token),
    INDEX idx_email_expires (email, expires_at)
);

-- Create an event to automatically clean up expired and used tokens after 24 hours
DELIMITER //
CREATE EVENT IF NOT EXISTS cleanup_reset_tokens
ON SCHEDULE EVERY 1 HOUR
DO
BEGIN
    DELETE FROM password_reset_tokens
    WHERE expires_at < NOW() - INTERVAL 24 HOUR
       OR used = TRUE;
END //
DELIMITER ;