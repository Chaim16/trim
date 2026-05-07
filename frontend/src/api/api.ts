import axiosInstance from "@/utils/axios";

const api = {
  // 数据概览
  getDashboard: async () => {
    const res = await axiosInstance.get("/api/dashboard");
    return res.data;
  },
  getWeightTrend: async () => {
    const res = await axiosInstance.get("/api/dashboard/weight_trend");
    return res.data;
  },

  // 体重记录
  getWeightRecord: async () => {
    const res = await axiosInstance.get("/api/weight_record");
    return res.data;
  },
  addWeightRecord: async (body: any) => {
    const res = await axiosInstance.post("/api/weight_record", body);
    return res.data;
  },
  deleteWeightRecord: async (id: number) => {
    const res = await axiosInstance.delete(`/api/weight_record/${id}`);
    return res.data;
  },

  // 食物管理
  getFood: async () => {
    const res = await axiosInstance.get("/api/food");
    return res.data;
  },

  // 饮食记录
  getFoodRecord: async (date: string) => {
    const res = await axiosInstance.get(`/api/food_record?date=${date}`);
    return res.data;
  },
  addFoodRecord: async (body: any) => {
    const res = await axiosInstance.post("/api/food_record", body);
    return res.data;
  },
  deleteFoodRecord: async (id: number) => {
    const res = await axiosInstance.delete(`/api/food_record/${id}`);
    return res.data;
  },

  // 运动记录
  getExerciseRecord: async (date: string) => {
    const res = await axiosInstance.get(`/api/exercise_record?date=${date}`);
    return res.data;
  },
  addExerciseRecord: async (body: any) => {
    const res = await axiosInstance.post("/api/exercise_record", body);
    return res.data;
  },
  deleteExerciseRecord: async (id: number) => {
    const res = await axiosInstance.delete(`/api/exercise_record/${id}`);
    return res.data;
  },
};

export default api;
