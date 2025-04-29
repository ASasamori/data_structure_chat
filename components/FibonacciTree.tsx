'use client';

import dynamic from 'next/dynamic';
import { useEffect, useState } from 'react';

const Tree = dynamic(() => import('react-d3-tree').then(mod => mod.Tree), { ssr: false });

export default function FibonacciTree({ data }: { data: any }) {
  const [treeData, setTreeData] = useState<any>(null);

  useEffect(() => {
    if (Array.isArray(data)) {
      setTreeData({ name: 'HeapRoots', children: data });
    } else if (data) {
      setTreeData(data);
    }
  }, [data]);

  if (!treeData) return <p>Loading tree...</p>;

  return (
    <div style={{ width: '100%', height: '600px' }}>
      <Tree
        data={treeData}
        orientation="vertical"
        translate={{ x: 400, y: 50 }}
      />
    </div>
  );
}
