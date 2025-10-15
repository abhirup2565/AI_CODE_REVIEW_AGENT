import { AlertCircle, CheckCircle, Clock, Loader2} from 'lucide-react';

const StatusBadge = ({ status }) => {
    //generate Icon colorClass and Spin properties depending on status
  const getConfig = (status) => {
    switch (status) {
      case 'PENDING':
        return { Icon: Clock, colorClass: 'bg-yellow-500/10 text-yellow-500 border-yellow-500/30' };
      case 'PROGRESS':
        return { Icon: Loader2, colorClass: 'bg-blue-500/10 text-blue-500 border-blue-500/30', spin: true };
      case 'SUCCESS':
        return { Icon: CheckCircle, colorClass: 'bg-green-500/10 text-green-500 border-green-500/30' };
      case 'FAILURE':
        return { Icon: AlertCircle, colorClass: 'bg-red-500/10 text-red-500 border-red-500/30' };
      default:
        return { Icon: Clock, colorClass: 'bg-gray-500/10 text-gray-500 border-gray-500/30' };
    }
  };

  const { Icon, colorClass, spin } = getConfig(status);

  return (
    <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ${colorClass}`}>
      <Icon className={`w-4 h-4 ${spin ? 'animate-spin' : ''}`} />
      <span className="ml-2">{status}</span>
    </div>
  );
};

export default StatusBadge