<template>
  <div class="home">
    <div class="page-header">
      <h1>个人减肥记录</h1>
      <p class="page-subtitle">健康生活，从记录开始</p>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-container">
      <div class="stat-card" v-for="(stat, index) in stats" :key="index">
        <div class="stat-icon">{{ stat.icon }}</div>
        <div class="stat-content">
          <div class="stat-title">{{ stat.title }}</div>
          <div class="stat-value">{{ stat.value }}</div>
        </div>
      </div>
    </div>

    <!-- 体重趋势图 -->
    <div class="chart-container">
      <div class="chart-header">
        <h2>体重变化趋势</h2>
        <p class="chart-subtitle">追踪你的减肥进度</p>
      </div>
      <div ref="chartRef" class="chart"></div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from "vue";
import * as echarts from "echarts";
import api from "@/api/api";

export default defineComponent({
  name: "HomeView",
  setup() {
    const chartRef = ref<HTMLElement | null>(null);
    const dashboardData = ref({
      current_weight: 0,
      target_weight: 70,
      today_food_calorie: 0,
      today_exercise_calorie: 0,
      today_net_calorie: 0,
    });

    // 计算统计数据
    const stats = computed(() => [
      {
        icon: "⚖️",
        title: "当前体重",
        value: `${dashboardData.value.current_weight} kg`,
      },
      {
        icon: "🎯",
        title: "目标体重",
        value: `${dashboardData.value.target_weight} kg`,
      },
      {
        icon: "🍽️",
        title: "今日摄入热量",
        value: `${dashboardData.value.today_food_calorie} kcal`,
      },
      {
        icon: "🏃‍♂️",
        title: "今日运动消耗",
        value: `${dashboardData.value.today_exercise_calorie} kcal`,
      },
      {
        icon: "⚡",
        title: "今日净热量",
        value: `${dashboardData.value.today_net_calorie} kcal`,
      },
    ]);

    // 获取仪表盘数据
    const getDashboardData = async () => {
      try {
        const res = await api.getDashboard();
        if (res.code === 0) {
          dashboardData.value = res.data;
        }
      } catch (error) {
        console.error("获取仪表盘数据失败:", error);
      }
    };

    // 获取体重趋势数据
    const getWeightTrendData = async () => {
      try {
        const res = await api.getWeightTrend();
        if (res.code === 0 && res.data.length > 0) {
          renderWeightChart(res.data);
        }
      } catch (error) {
        console.error("获取体重趋势数据失败:", error);
      }
    };

    // 渲染体重趋势图
    const renderWeightChart = (data: any[]) => {
      if (!chartRef.value) return;

      const chart = echarts.init(chartRef.value);

      const dates = data.map((item) => item.date);
      const weights = data.map((item) => item.weight);

      const option = {
        tooltip: {
          trigger: "axis",
          formatter: function (params: any) {
            return `${params[0].name}<br/>体重: ${params[0].value} kg`;
          },
          backgroundColor: "rgba(255, 255, 255, 0.95)",
          borderColor: "#e9ecef",
          borderWidth: 1,
          padding: 12,
          textStyle: {
            color: "#333",
          },
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "15%",
          top: "10%",
          containLabel: true,
        },
        xAxis: {
          type: "category",
          data: dates,
          axisLabel: {
            rotate: 45,
            color: "#666",
            fontSize: 12,
          },
          axisLine: {
            lineStyle: {
              color: "#e9ecef",
            },
          },
          axisTick: {
            show: false,
          },
        },
        yAxis: {
          type: "value",
          name: "体重 (kg)",
          nameTextStyle: {
            color: "#666",
            fontSize: 12,
          },
          axisLabel: {
            color: "#666",
            fontSize: 12,
          },
          axisLine: {
            lineStyle: {
              color: "#e9ecef",
            },
          },
          axisTick: {
            show: false,
          },
          splitLine: {
            lineStyle: {
              color: "#f1f3f5",
              type: "dashed",
            },
          },
        },
        series: [
          {
            data: weights,
            type: "line",
            smooth: true,
            symbol: "circle",
            symbolSize: 8,
            lineStyle: {
              width: 3,
              color: "#409EFF",
            },
            itemStyle: {
              color: "#409EFF",
              borderColor: "#fff",
              borderWidth: 2,
            },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {
                  offset: 0,
                  color: "rgba(64, 158, 255, 0.3)",
                },
                {
                  offset: 1,
                  color: "rgba(64, 158, 255, 0.05)",
                },
              ]),
            },
          },
        ],
      };

      chart.setOption(option);

      // 响应式调整
      window.addEventListener("resize", () => {
        chart.resize();
      });
    };

    onMounted(() => {
      getDashboardData();
      getWeightTrendData();
    });

    return {
      chartRef,
      dashboardData,
      stats,
    };
  },
});
</script>

<style scoped>
.home {
  padding: 0 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
  padding: 20px 0;
}

.page-header h1 {
  color: #333;
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 10px;
  animation: fadeInDown 0.8s ease;
}

.page-subtitle {
  color: #666;
  font-size: 16px;
  animation: fadeInUp 0.8s ease 0.2s both;
}

.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: #fff;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  gap: 15px;
  transition: all 0.3s ease;
  animation: fadeInUp 0.6s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.stat-card:nth-child(1) {
  animation-delay: 0.1s;
}

.stat-card:nth-child(2) {
  animation-delay: 0.2s;
}

.stat-card:nth-child(3) {
  animation-delay: 0.3s;
}

.stat-card:nth-child(4) {
  animation-delay: 0.4s;
}

.stat-card:nth-child(5) {
  animation-delay: 0.5s;
}

.stat-icon {
  font-size: 32px;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  border-radius: 50%;
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
}

.stat-title {
  font-size: 14px;
  color: #666;
  margin-bottom: 5px;
  font-weight: 500;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  line-height: 1.2;
}

.chart-container {
  background: #fff;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  animation: fadeInUp 0.8s ease 0.6s both;
}

.chart-header {
  margin-bottom: 20px;
}

.chart-header h2 {
  color: #333;
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 5px;
}

.chart-subtitle {
  color: #666;
  font-size: 14px;
}

.chart {
  width: 100%;
  height: 400px;
}

/* 动画效果 */
@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .page-header h1 {
    font-size: 24px;
  }

  .page-subtitle {
    font-size: 14px;
  }

  .stats-container {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 15px;
  }

  .stat-card {
    padding: 20px;
  }

  .stat-icon {
    font-size: 24px;
    width: 50px;
    height: 50px;
  }

  .stat-title {
    font-size: 13px;
  }

  .stat-value {
    font-size: 20px;
  }

  .chart-container {
    padding: 20px;
  }

  .chart-header h2 {
    font-size: 18px;
  }

  .chart-subtitle {
    font-size: 13px;
  }

  .chart {
    height: 300px;
  }
}

@media (max-width: 480px) {
  .page-header h1 {
    font-size: 20px;
  }

  .page-subtitle {
    font-size: 13px;
  }

  .stats-container {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .stat-card {
    flex-direction: column;
    text-align: center;
    gap: 10px;
    padding: 16px;
  }

  .stat-icon {
    font-size: 20px;
    width: 40px;
    height: 40px;
  }

  .stat-title {
    font-size: 12px;
  }

  .stat-value {
    font-size: 18px;
  }

  .chart-container {
    padding: 16px;
  }

  .chart-header h2 {
    font-size: 16px;
  }

  .chart {
    height: 200px;
  }
}
</style>
