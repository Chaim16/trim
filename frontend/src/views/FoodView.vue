<template>
  <div class="food-view">
    <div class="page-header">
      <h1>饮食记录管理</h1>
      <p class="page-subtitle">记录你的饮食摄入，控制热量平衡</p>
    </div>

    <!-- 添加饮食记录 -->
    <div class="add-form">
      <div class="form-header">
        <h2>添加饮食记录</h2>
        <p class="form-subtitle">记录你的每日饮食</p>
      </div>
      <form @submit.prevent="addFoodRecord">
        <div class="form-row">
          <div class="form-item">
            <label for="date">日期</label>
            <input
              type="date"
              id="date"
              v-model="newFoodRecord.date"
              required
              class="form-input"
            />
          </div>
          <div class="form-item">
            <label for="food_id">食物</label>
            <select
              id="food_id"
              v-model="newFoodRecord.food_id"
              required
              class="form-input"
            >
              <option value="">请选择食物</option>
              <option v-for="food in foods" :key="food.id" :value="food.id">
                {{ food.name }} ({{ food.calorie_per_100g }} kcal/100g)
              </option>
            </select>
          </div>
          <div class="form-item">
            <label for="weight">重量 (g)</label>
            <input
              type="number"
              id="weight"
              v-model.number="newFoodRecord.weight"
              step="1"
              required
              class="form-input"
            />
          </div>
          <div class="form-item form-submit">
            <button type="submit" class="btn btn-primary">添加记录</button>
          </div>
        </div>
      </form>
    </div>

    <!-- 饮食记录列表 -->
    <div class="record-list">
      <div class="list-header">
        <h2>今日饮食记录</h2>
        <p class="list-subtitle">查看你的饮食摄入</p>
      </div>
      <div class="date-selector">
        <label for="record-date">选择日期</label>
        <input
          type="date"
          id="record-date"
          v-model="selectedDate"
          @change="getFoodRecords"
          class="form-input date-input"
        />
      </div>
      <div class="table-container">
        <table class="table">
          <thead>
            <tr>
              <th>食物名称</th>
              <th>重量 (g)</th>
              <th>热量 (kcal)</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="record in foodRecords"
              :key="record.id"
              class="table-row"
            >
              <td>{{ record.food_name }}</td>
              <td>{{ record.weight }}</td>
              <td>{{ record.calorie }}</td>
              <td>
                <button
                  class="btn btn-danger"
                  @click="deleteFoodRecord(record.id)"
                >
                  删除
                </button>
              </td>
            </tr>
            <tr v-if="foodRecords.length === 0">
              <td colspan="4" class="empty">
                <div class="empty-state">
                  <span class="empty-icon">🍎</span>
                  <p>暂无饮食记录</p>
                  <p class="empty-hint">点击上方添加按钮开始记录</p>
                </div>
              </td>
            </tr>
          </tbody>
          <tfoot>
            <tr>
              <td colspan="2" class="total-label">总计</td>
              <td class="total-value">{{ totalCalorie }} kcal</td>
              <td></td>
            </tr>
          </tfoot>
        </table>
      </div>
    </div>

    <!-- 食物列表 -->
    <div class="food-list">
      <div class="list-header">
        <h2>食物列表</h2>
        <p class="list-subtitle">常见食物热量参考</p>
      </div>
      <div class="table-container">
        <table class="table">
          <thead>
            <tr>
              <th>食物名称</th>
              <th>热量 (kcal/100g)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="food in foods" :key="food.id" class="table-row">
              <td>{{ food.name }}</td>
              <td>{{ food.calorie_per_100g }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from "vue";
import api from "@/api/api";

export default defineComponent({
  name: "FoodView",
  setup() {
    const foods = ref<any[]>([]);
    const foodRecords = ref<any[]>([]);
    const selectedDate = ref(new Date().toISOString().split("T")[0]);
    const newFoodRecord = ref({
      date: new Date().toISOString().split("T")[0],
      food_id: "",
      weight: 0,
    });

    // 计算总热量
    const totalCalorie = computed(() => {
      return foodRecords.value.reduce((sum, record) => sum + record.calorie, 0);
    });

    // 获取食物列表
    const getFoods = async () => {
      try {
        const res = await api.getFood();
        if (res.code === 0) {
          foods.value = res.data;
        }
      } catch (error) {
        console.error("获取食物列表失败:", error);
      }
    };

    // 获取饮食记录
    const getFoodRecords = async () => {
      try {
        const res = await api.getFoodRecord(selectedDate.value);
        if (res.code === 0) {
          foodRecords.value = res.data;
        }
      } catch (error) {
        console.error("获取饮食记录失败:", error);
      }
    };

    // 添加饮食记录
    const addFoodRecord = async () => {
      try {
        const res = await api.addFoodRecord(newFoodRecord.value);
        if (res.code === 0) {
          // 重置表单
          newFoodRecord.value = {
            date: new Date().toISOString().split("T")[0],
            food_id: "",
            weight: 0,
          };
          // 重新获取记录列表
          getFoodRecords();
        }
      } catch (error) {
        console.error("添加饮食记录失败:", error);
      }
    };

    // 删除饮食记录
    const deleteFoodRecord = async (id: number) => {
      try {
        const res = await api.deleteFoodRecord(id);
        if (res.code === 0) {
          // 重新获取记录列表
          getFoodRecords();
        }
      } catch (error) {
        console.error("删除饮食记录失败:", error);
      }
    };

    onMounted(() => {
      getFoods();
      getFoodRecords();
    });

    return {
      foods,
      foodRecords,
      selectedDate,
      newFoodRecord,
      totalCalorie,
      getFoodRecords,
      addFoodRecord,
      deleteFoodRecord,
    };
  },
});
</script>

<style scoped>
.food-view {
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

.date-input {
  width: auto;
  min-width: 180px;
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

.date-selector {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.date-selector label {
  color: #666;
  font-weight: 500;
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

.table tfoot {
  font-weight: bold;
  background-color: #f8f9fa;
}

.total-label {
  text-align: right;
  color: #333;
}

.total-value {
  color: #409eff;
  font-weight: bold;
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

.food-list {
  background: #fff;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  animation: fadeInUp 0.6s ease 0.3s both;
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
  .food-list {
    padding: 20px;
  }

  .form-header h2,
  .list-header h2 {
    font-size: 18px;
  }

  .form-subtitle,
  .list-subtitle {
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

  .date-selector {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .date-input {
    width: 100%;
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
  .food-list {
    padding: 16px;
  }

  .form-header h2,
  .list-header h2 {
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

  .btn-danger {
    padding: 4px 8px;
    font-size: 11px;
  }

  .table th,
  .table td {
    padding: 10px;
    font-size: 13px;
  }

  .empty-icon {
    font-size: 36px;
  }

  .empty-state p {
    font-size: 13px;
  }
}
</style>
