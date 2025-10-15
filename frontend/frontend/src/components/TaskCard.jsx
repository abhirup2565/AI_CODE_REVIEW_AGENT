const TaskCard = ({ task, onViewResult, onDelete, showDelete = false }) => {
  return (
    <div className="bg-gray-800/50 backdrop-blur p-6 rounded-lg border border-gray-700 hover:border-gray-600 transition-all">
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="flex items-center mb-2">
            <Github className="w-4 h-4 text-gray-400 mr-2" />
            <span className="text-sm text-gray-300">PR #{task.pr_number}</span>
          </div>
          <p className="text-xs text-gray-500 mb-2 truncate">{task.repo_url}</p>
          <code className="text-xs bg-gray-900 px-2 py-1 rounded text-blue-400 font-mono">
            {task.task_id}
          </code>
        </div>
        {showDelete && (
          <button
            onClick={() => onDelete(task.task_id)}
            className="text-red-400 hover:text-red-300 p-2 hover:bg-red-900/20 rounded transition-colors"
            title="Delete task"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        )}
      </div>

      <div className="flex items-center justify-between mb-4">
        <StatusBadge status={task.status || task.state} />
        {task.created_at && (
          <span className="text-xs text-gray-500">{formatDate(task.created_at)}</span>
        )}
      </div>

      {(task.status === 'SUCCESS' || task.state === 'SUCCESS') && (
        <button
          onClick={() => onViewResult(task.task_id)}
          className="w-full px-4 py-2 bg-green-600 hover:bg-green-700 text-white font-medium rounded-lg transition-all flex items-center justify-center"
        >
          <Eye className="w-4 h-4 mr-2" />
          View Results
        </button>
      )}

      {(task.status === 'FAILURE' || task.state === 'FAILURE') && (
        <div className="p-3 bg-red-900/20 border border-red-700 rounded-lg text-red-300 text-sm">
          Analysis failed. Please try again.
        </div>
      )}
    </div>
  );
};
export default TaskCard