import React, { useContext, useEffect, useState } from 'react';
import { Box, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from '@mui/material';
import { TableComponents, TableVirtuoso } from 'react-virtuoso';
import { getHistory } from '../../services/admin';
import AuthContext from '../../context/AuthContext';

const columns: ColumnData[] = [
  {
    width: 100,
    label: 'ID',
    dataKey: 'imageID',
  },
  {
    width: 200,
    label: 'Image',
    dataKey: 'imageURL',
  },
  {
    width: 100,
    label: 'Result',
    dataKey: 'result',
  },
  {
    width: 200,
    label: 'Timestamp',
    dataKey: 'verificationTimestamp',
  }
]

function fixedHeaderContent() {
  return (
    <TableRow>
      {columns.map((column) => (
        <TableCell
          key={column.dataKey}
          variant="head"
          align={column.numeric || false ? 'right' : 'left'}
          style={{ width: column.width }}
          sx={{
            backgroundColor: 'background.paper',
          }}
        >
          {column.label}
        </TableCell>
      ))}
    </TableRow>
  );
}

const HistoryTab: React.FC = () => {
  const [history, setHistory] = useState<any[]>([]);
  const { user } = useContext(AuthContext);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    const data = await getHistory(user?.uid ?? '');
    console.log('History', data);
    setHistory(data);
  };

  const VirtuosoTableComponents: TableComponents<VerificationResult> = {
    Scroller: React.forwardRef<HTMLDivElement>((props, ref) => (
      <TableContainer component={Paper} {...props} ref={ref} />
    )),
    Table: (props) => (
      <Table {...props} sx={{ borderCollapse: 'separate', tableLayout: 'fixed' }} />
    ),
    TableHead: React.forwardRef<HTMLTableSectionElement>((props, ref) => (
      <TableHead {...props} ref={ref} />
    )),
    TableRow,
    TableBody: React.forwardRef<HTMLTableSectionElement>((props, ref) => (
      <TableBody {...props} ref={ref} />
    )),
  };

  return (
    <Box p={3}>
      <TableContainer component={Paper} style={{ height: 600 }}>
        <TableVirtuoso
          data={history}
          components={VirtuosoTableComponents}
          fixedHeaderContent={fixedHeaderContent}
          itemContent={(index: number, row: any) => (
            <React.Fragment>
              <TableCell>{row.imageID}</TableCell>
              <TableCell>
                <img src={row.imageURL} alt="Thumbnail" height="50" />
              </TableCell>
              <TableCell>{row.result === 0 ? 'PASS' : 'FAIL'}</TableCell>
              <TableCell>{new Date(row.verificationTimestamp).toLocaleString()}</TableCell>
            </React.Fragment>
          )}
        />
      </TableContainer>
    </Box>
  );
};

export default HistoryTab;
