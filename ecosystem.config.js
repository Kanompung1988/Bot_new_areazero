/**
 * PM2 Ecosystem Configuration for Python Discord Bot
 * ใช้ PM2 รัน Python bot แบบ production-ready
 * 
 * Installation:
 * npm install -g pm2
 * 
 * Usage:
 * pm2 start ecosystem.config.js
 * pm2 status
 * pm2 logs bot
 * pm2 restart bot
 * pm2 stop bot
 * pm2 delete bot
 * 
 * Auto-start on system boot:
 * pm2 startup
 * pm2 save
 */

module.exports = {
  apps: [
    {
      name: 'bot',
      script: 'python',
      args: 'run_bot.py',
      interpreter: 'none',  // ไม่ใช้ node interpreter
      
      // Auto-restart settings
      autorestart: true,
      watch: false,  // ไม่ต้อง watch files (เปลี่ยนเป็น true ถ้าต้องการ auto-reload)
      max_restarts: 10,  // จำนวนครั้งสูงสุดที่ restart ใน 1 นาที
      min_uptime: '10s',  // ต้องรันได้อย่างน้อย 10 วินาทีถึงจะถือว่า restart สำเร็จ
      restart_delay: 5000,  // รอ 5 วินาทีก่อน restart
      
      // Exponential backoff restart delay
      exp_backoff_restart_delay: 100,
      max_memory_restart: '500M',  // Restart ถ้าใช้ memory เกิน 500MB
      
      // Error handling
      error_file: 'logs/pm2-error.log',
      out_file: 'logs/pm2-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      
      // Environment
      env: {
        NODE_ENV: 'production',
        PYTHONUNBUFFERED: '1',  // ทำให้ Python output แสดงทันที
      },
      
      // Keep-alive strategy
      kill_timeout: 5000,  // รอ 5 วินาทีก่อน force kill
      listen_timeout: 10000,  // รอ 10 วินาทีให้ app พร้อม
      
      // Cron restart (optional) - restart ทุกวันเวลา 03:00
      // cron_restart: '0 3 * * *',
      
      // Instance management
      instances: 1,  // รัน 1 instance (bot ควรรัน single instance)
      exec_mode: 'fork',  // ใช้ fork mode สำหรับ Python
    },
    
    // API Server (optional - ถ้าต้องการรัน API server แยก)
    {
      name: 'api',
      script: 'python',
      args: 'main.py --api',
      interpreter: 'none',
      
      autorestart: true,
      watch: false,
      max_restarts: 10,
      min_uptime: '10s',
      restart_delay: 5000,
      
      error_file: 'logs/pm2-api-error.log',
      out_file: 'logs/pm2-api-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      
      env: {
        NODE_ENV: 'production',
        PYTHONUNBUFFERED: '1',
        PORT: '8000',
      },
      
      instances: 1,
      exec_mode: 'fork',
    }
  ]
};
