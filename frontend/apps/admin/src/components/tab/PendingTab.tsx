import React, { useState, useEffect, useMemo, useContext } from 'react';
import { Button, Box, Typography, Paper, IconButton } from '@mui/material';
import { List, AutoSizer } from 'react-virtualized';
import { getPendingImages, verifyImage } from '../../services/admin';
import AuthContext from '../../context/AuthContext';

interface Image {
  filename: string;
  imageID: number;
  references: any[];
}

const PendingTab: React.FC = () => {
  const [pendingImages, setPendingImages] = useState<Image[]>([
    {
      filename: "",
      imageID: 0,
      references: [{filename: "", imageID: 0}]
    }
  ]);

  const { user } = useContext(AuthContext);

  useEffect(() => {
    fetchPendingImages();
  }, []);

  const fetchPendingImages = async () => {
    const data = await getPendingImages();
    console.log('Pending images', data);
    setPendingImages(data);
  };

  const handleVerify = async (result: number) => {
    if (!pendingImages[0]) return;

    await verifyImage(pendingImages[0].imageID, user?.uid ?? "", result);
    fetchPendingImages();
  };

  const renderRow = ({ index, key, style }: any) => {
    if (!pendingImages || !pendingImages[0] || !pendingImages[0].references) return null;
    const image = pendingImages[0].references[index];
    return (
      <div key={key} style={style}>
        <img src={image.filename} alt={`Pending ${index}`} width="50" height="50" />
      </div>
    );
  };

  return (
    <Box display="flex" p={2}>
      <Box flexGrow={1}>
        {pendingImages[0] && (
          <Paper elevation={3} style={{ padding: 16 }}>
            <img src={pendingImages[0].filename} alt="Current" width="300" height="300" />
            <Box mt={2}>
              <Button
                variant="contained"
                color="primary"
                onClick={() => handleVerify(1)}
                style={{ marginRight: 16 }}
              >
                PASS
              </Button>
              <Button variant="contained" color="secondary" onClick={() => handleVerify(0)}>
                FAIL
              </Button>
            </Box>
          </Paper>
        )}
      </Box>
      <Box width="300px" height="500px" ml={2}>
        <AutoSizer>
          {({ height, width }) => (
            <List
              height={height}
              rowCount={(pendingImages && pendingImages[0].references ? pendingImages[0].references.length : 1)}
              rowHeight={60}
              rowRenderer={renderRow}
              width={width}
            />
          )}
        </AutoSizer>
      </Box>
    </Box>
  );
};

export default PendingTab;
