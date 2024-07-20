import React, { useEffect, useState } from 'react';
import { Box, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from '@mui/material';
import { TableVirtuoso } from 'react-virtuoso';
// import { getHistory } from '../services/admin'; // Ensure to create this function in your service file

const HistoryTab: React.FC = () => {
  const [history, setHistory] = useState<any[]>([]);

  // useEffect(() => {
  //   fetchHistory();
  // }, []);

  // const fetchHistory = async () => {
  //   const data = await getHistory();
  //   setHistory(data);
  // };

  return (
    <Box p={3}>
      <TableContainer component={Paper} style={{ height: 600 }}>
        <TableVirtuoso
          data={history}
          components={{
            Scroller: React.forwardRef<any>((props, ref) => <TableContainer  component={Paper} {...props} ref={ref} />),
            Table: (props : any) => <Table {...props} component="div" />,
            TableHead,
            TableRow: (props: any) => <TableRow {...props} component="div" />,
            TableBody: React.forwardRef<any>((props, ref) => <TableBody {...props} ref={ref} component="div" />),
          }}
          fixedHeaderContent={() => (
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Image</TableCell>
              <TableCell>Admin UID</TableCell>
              <TableCell>Result</TableCell>
              <TableCell>Timestamp</TableCell>
            </TableRow>
          )}
          itemContent={(index: number, row: any) => (
            <>
              <TableCell>{row.id}</TableCell>
              <TableCell>
                <img src={row.imageId} alt="Thumbnail" width="50" height="50" />
              </TableCell>
              <TableCell>{row.adminUID}</TableCell>
              <TableCell>{row.result === 1 ? 'PASS' : 'FAIL'}</TableCell>
              <TableCell>{new Date(row.timestamp).toLocaleString()}</TableCell>
            </>
          )}
        />
      </TableContainer>
    </Box>
  );
};

export default HistoryTab;
