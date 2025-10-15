const storage = {
  setAccessToken: (token) => localStorage.setItem('access_token', token),
  getAccessToken: () => localStorage.getItem('access_token'),
  clearAccessToken: () => localStorage.removeItem('access_token'),
  setOngoingTasks: (tasks) => localStorage.setItem('ongoing_tasks', JSON.stringify(tasks)),
  getOngoingTasks: () => {
    const tasks = localStorage.getItem('ongoing_tasks');
    return tasks ? JSON.parse(tasks) : [];
  },
  addOngoingTask: (task) => {
    const tasks = storage.getOngoingTasks();
    tasks.push(task);
    storage.setOngoingTasks(tasks);
  },
  removeOngoingTask: (taskId) => {
    const tasks = storage.getOngoingTasks();
    storage.setOngoingTasks(tasks.filter(t => t.task_id !== taskId));
  }
};

export default storage;