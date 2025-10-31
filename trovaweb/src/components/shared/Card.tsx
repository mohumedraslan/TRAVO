import React from 'react';

interface CardProps {
  title: string;
  description?: string;
  onClick?: () => void;
}

export const Card: React.FC<CardProps> = ({ title, description, onClick }) => {
  return (
    <div className="rounded-lg border border-zinc-200 bg-white p-4 shadow-sm hover:shadow-md dark:border-zinc-800 dark:bg-zinc-900" onClick={onClick}>
      <h3 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">{title}</h3>
      {description && (
        <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">{description}</p>
      )}
    </div>
  );
};

export default Card;