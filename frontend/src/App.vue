<template>
  <div id="app">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="navbar-container">
        <a href="/" class="navbar-brand">
          <span class="brand-icon">🏋️‍♀️</span>
          <span class="brand-text">减简</span>
        </a>
        <div class="navbar-nav">
          <router-link to="/" class="nav-link">
            <span class="link-icon">📊</span>
            <span class="link-text">概览</span>
          </router-link>
          <router-link to="/weight" class="nav-link">
            <span class="link-icon">⚖️</span>
            <span class="link-text">体重记录</span>
          </router-link>
          <router-link to="/food" class="nav-link">
            <span class="link-icon">🍎</span>
            <span class="link-text">饮食记录</span>
          </router-link>
          <router-link to="/exercise" class="nav-link">
            <span class="link-icon">🏃‍♂️</span>
            <span class="link-text">运动记录</span>
          </router-link>
        </div>
      </div>
    </nav>

    <!-- 内容区域 -->
    <main class="main">
      <router-view />
    </main>

    <!-- 页脚 -->
    <footer class="footer">
      <div class="footer-container">
        <p>&copy; 2026 减简 | 健康生活，从记录开始</p>
      </div>
    </footer>
  </div>
</template>

<script lang="ts">
export default {
  name: "App",
};
</script>

<style>
/* 全局样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f8f9fa;
  color: #333;
  line-height: 1.6;
}

/* 导航栏样式 */
.navbar {
  background: linear-gradient(135deg, #409eff, #667eea);
  color: #fff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
  transition: all 0.3s ease;
}

.navbar:hover {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 70px;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 22px;
  font-weight: bold;
  color: #fff;
  text-decoration: none;
  transition: transform 0.3s ease;
}

.navbar-brand:hover {
  transform: translateY(-2px);
}

.brand-icon {
  font-size: 24px;
}

.navbar-nav {
  display: flex;
  gap: 15px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #fff;
  text-decoration: none;
  padding: 10px 18px;
  border-radius: 25px;
  transition: all 0.3s ease;
  font-weight: 500;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.nav-link.router-link-active {
  background-color: rgba(255, 255, 255, 0.25);
  font-weight: bold;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.link-icon {
  font-size: 16px;
}

/* 内容区域样式 */
.main {
  min-height: calc(100vh - 120px);
  padding: 30px 0;
}

/* 页脚样式 */
.footer {
  background-color: #f1f3f5;
  border-top: 1px solid #e9ecef;
  padding: 20px 0;
  margin-top: 30px;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
  color: #6c757d;
  font-size: 14px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .navbar-container {
    flex-direction: column;
    height: auto;
    padding: 15px 20px;
    gap: 10px;
  }

  .navbar-nav {
    flex-wrap: wrap;
    justify-content: center;
    gap: 10px;
  }

  .nav-link {
    padding: 8px 14px;
    font-size: 14px;
  }

  .main {
    min-height: calc(100vh - 180px);
    padding: 20px 0;
  }
}

@media (max-width: 480px) {
  .navbar-brand {
    font-size: 18px;
  }

  .brand-icon {
    font-size: 20px;
  }

  .navbar-nav {
    gap: 8px;
  }

  .nav-link {
    padding: 6px 10px;
    font-size: 12px;
    border-radius: 20px;
  }

  .link-text {
    display: none;
  }

  .footer-container {
    font-size: 12px;
    padding: 0 20px;
  }
}
</style>
