<template>
  <div class="weight-view">
    <div class="page-header">
      <h1>体重记录管理</h1>
      <p class="page-subtitle">记录你的体重变化，追踪减肥进度</p>
    </div>

    <!-- 添加体重记录 -->
    <div class="add-form">
      <div class="form-header">
        <h2>添加体重记录</h2>
        <p class="form-subtitle">记录你的每日体重</p>
      </div>
      <form @submit.prevent="addWeightRecord">
        <div class="form-row">
          <div class="form-item">
            <label for="date">日期</label>
            <input
              type="date"
              id="date"
              v-model="newWeightRecord.date"
              required
              class="form-input"
            />
          </div>
          <div class="form-item">
            <label for="weight">体重 (kg)</label>
            <input
              type="number"
              id="weight"
              v-model.number="newWeightRecord.weight"
              step="0.1"
              required
              class="form-input"
            />
          </div>
          <div class="form-item">
            <label for="note">备注</label>
            <input
              type="text"
              id="note"
              v-model="newWeightRecord.note"
              class="form-input"
              placeholder="例如：晨起体重"
            />
          </div>
          <div class="form-item form-submit">
            <button type="submit" class="btn btn-primary">添加记录</button>
          </div>
        </div>
      </form>
    </div>

    <!-- 体重记录列表 -->
    <div class="record-list">
      <div class="list-header">
        <h2>历史体重记录</h2>
        <p class="list-subtitle">查看你的体重变化历史</p>
      </div>
      <div class="table-container">
        <table class="table">
          <thead>
            <tr>
              <th>日期</th>
              <th>体重 (kg)</th>
              <th>备注</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="record in weightRecords"
              :key="record.id"
              class="table-row"
            >
              <td>{{ record.date }}</td>
              <td>{{ record.weight }}</td>
              <td>{{ record.note || "-" }}</td>
              <td>
                <button
                  class="btn btn-danger"
                  @click="deleteWeightRecord(record.id)"
                >
                  删除
                </button>
              </td>
            </tr>
            <tr v-if="weightRecords.length === 0">
              <td colspan="4" class="empty">
                <div class="empty-state">
                  <span class="empty-icon">📋</span>
                  <p>暂无体重记录</p>
                  <p class="empty-hint">点击上方添加按钮开始记录</p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 体重趋势图 -->
    <div class="chart-container">
      <div class="chart-header">
        <h2>体重变化趋势</h2>
        <p class="chart-subtitle">直观了解你的减肥进度</p>
      </div>
      <div ref="chartRef" class="chart"></div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import * as echarts from "echarts";
import api from "@/api/api";

export default defineComponent({
  name: "WeightView",
  setup() {
    const chartRef = ref<HTMLElement | null>(null);
    const weightRecords = ref<any[]>([]);
    const newWeightRecord = ref({
      date: new Date().toISOString().split("T")[0],
      weight: 0,
      note: "",
    });

    // 获取体重记录列表
    const getWeightRecords = async () => {
      try {
        const res = await api.getWeightRecord();
        if (res.code === 0) {
          weightRecords.value = res.data;
          renderWeightChart(res.data);
        }
      } catch (error) {
        console.error("获取体重记录失败:", error);
      }
    };

    // 添加体重记录
    const addWeightRecord = async () => {
      try {
        const res = await api.addWeightRecord(newWeightRecord.value);
        if (res.code === 0) {
          // 重置表单
          newWeightRecord.value = {
            date: new Date().toISOString().split("T")[0],
            weight: 0,
            note: "",
          };
          // 重新获取记录列表
          getWeightRecords();
        }
      } catch (error) {
        console.error("添加体重记录失败:", error);
      }
    };

    // 删除体重记录
    const deleteWeightRecord = async (id: number) => {
      try {
        const res = await api.deleteWeightRecord(id);
        if (res.code === 0) {
          // 重新获取记录列表
          getWeightRecords();
        }
      } catch (error) {
        console.error("删除体重记录失败:", error);
      }
    };

    // 渲染体重趋势图
    const renderWeightChart = (data: any[]) => {
      if (!chartRef.value || data.length === 0) return;

      const chart = echarts.init(chartRef.value);

      // 按日期排序
      const sortedData = [...data].sort(
        (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()
      );
      const dates = sortedData.map((item) => item.date);
      const weights = sortedData.map((item) => item.weight);

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
      getWeightRecords();
    });

    return {
      chartRef,
      weightRecords,
      newWeightRecord,
      addWeightRecord,
      deleteWeightRecord,
    };
  },
});
</script>

<style scoped>
.weight-view {
  padding: 0 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
  padding: 20px 0;
  animation: fadeInDown 0.8s ease;
}

.page-header h1 {
  color: #333;
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 10px;
}

.page-subtitle {
  color: #666;
  font-size: 16px;
}

.add-form {
  background: #fff;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  margin-bottom: 30px;
  animation: fadeInUp 0.6s ease 0.1s both;
}

.form-header {
  margin-bottom: 20px;
}

.form-header h2 {
  color: #333;
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 5px;
}

.form-subtitle {
  color: #666;
  font-size: 14px;
}

.form-row {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.form-item {
  flex: 1;
  min-width: 200px;
}

.form-item label {
  display: block;
  margin-bottom: 8px;
  color: #666;
  font-weight: 500;
  font-size: 14px;
}

.form-input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.3s ease;
  background-color: #f8f9fa;
}

.form-input:focus {
  outline: none;
  border-color: #409eff;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.1);
  background-color: #fff;
}

.form-submit {
  display: flex;
  align-items: flex-end;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: linear-gradient(135deg, #409eff, #667eea);
  color: #fff;
  box-shadow: 0 4px 6px rgba(64, 158, 255, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(64, 158, 255, 0.4);
}

.btn-danger {
  background-color: #f56c6c;
  color: #fff;
  padding: 6px 12px;
  font-size: 12px;
  box-shadow: 0 2px 4px rgba(245, 108, 108, 0.3);
}

.btn-danger:hover {
  background-color: #f78989;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(245, 108, 108, 0.4);
}

.record-list {
  background: #fff;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  margin-bottom: 30px;
  animation: fadeInUp 0.6s ease 0.2s both;
}

.list-header {
  margin-bottom: 20px;
}

.list-header h2 {
  color: #333;
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 5px;
}

.list-subtitle {
  color: #666;
  font-size: 14px;
}

.table-container {
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.table th,
.table td {
  padding: 15px;
  text-align: left;
  border-bottom: 1px solid #f1f3f5;
}

.table th {
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  font-weight: bold;
  color: #333;
  font-size: 14px;
  position: sticky;
  top: 0;
  z-index: 10;
}

.table-row {
  transition: all 0.3s ease;
}

.table-row:hover {
  background-color: #f8f9fa;
  transform: translateY(-1px);
}

.empty {
  text-align: center;
  padding: 60px 20px;
  background-color: #f8f9fa;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 10px;
}

.empty-state p {
  color: #666;
  font-size: 16px;
}

.empty-hint {
  font-size: 14px;
  color: #999;
}

.chart-container {
  background: #fff;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  animation: fadeInUp 0.6s ease 0.3s both;
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

  .add-form,
  .record-list,
  .chart-container {
    padding: 20px;
  }

  .form-header h2,
  .list-header h2,
  .chart-header h2 {
    font-size: 18px;
  }

  .form-subtitle,
  .list-subtitle,
  .chart-subtitle {
    font-size: 13px;
  }

  .form-row {
    flex-direction: column;
    gap: 15px;
  }

  .form-item {
    min-width: 100%;
  }

  .form-item label {
    font-size: 13px;
  }

  .form-input {
    padding: 8px 10px;
    font-size: 13px;
  }

  .form-submit {
    align-items: center;
  }

  .btn {
    padding: 8px 16px;
    font-size: 13px;
  }

  .table th,
  .table td {
    padding: 12px;
    font-size: 14px;
  }

  .empty-state p {
    font-size: 14px;
  }

  .empty-hint {
    font-size: 12px;
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

  .add-form,
  .record-list,
  .chart-container {
    padding: 16px;
  }

  .form-header h2,
  .list-header h2,
  .chart-header h2 {
    font-size: 16px;
  }

  .form-row {
    gap: 12px;
  }

  .form-input {
    padding: 7px 9px;
    font-size: 12px;
  }

  .btn {
    padding: 7px 14px;
    font-size: 12px;
  }

  .table th,
  .table td {
    padding: 10px;
    font-size: 13px;
  }

  .btn-danger {
    padding: 4px 8px;
    font-size: 11px;
  }

  .empty-icon {
    font-size: 36px;
  }

  .empty-state p {
    font-size: 13px;
  }

  .chart {
    height: 200px;
  }
}
</style>
