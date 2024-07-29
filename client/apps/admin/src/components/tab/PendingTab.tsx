import React, { useState, useEffect, useMemo, useContext } from 'react';
import { Button, Box, Typography, Paper, IconButton } from '@mui/material';
import { List, AutoSizer } from 'react-virtualized';
import { getPendingImages, verifyImage } from '../../services/admin';
import AuthContext from '../../context/AuthContext';

interface Image {
  imageURL: string;
  imageID: number;
  refFilepaths: string[];
}

const PendingTab: React.FC = () => {
  const [pendingImages, setPendingImages] = useState<Image[]>([
    {
      imageURL: "",
      imageID: 0,
      refFilepaths: []
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
    console.log('Verifying image', pendingImages[0].imageID, result);
    await verifyImage(pendingImages[0].imageID, user?.uid ?? "", result);
    fetchPendingImages();
  };

  const renderRow = ({ index, key, style }: any) => {
    if (!pendingImages || !pendingImages[0] || !pendingImages[0].refFilepaths) return null;
    const image = pendingImages[0].refFilepaths[index];
    return (
      <div key={key} style={style}>
        <img src={image} alt={`Pending ${index}`} height="300px"/>
      </div>
    );
  };

  return (
    <Box display="flex" p={2}>
      <Box flexGrow={1} >
        {pendingImages[0] && (
          <Paper elevation={5} style={{ padding: 16, display: "flex", flexDirection: "column", alignItems: "center" }}>
            {pendingImages[0].imageURL ? <img src={pendingImages[0].imageURL} alt="Current" style={{ maxWidth: "700px"}} height="300" /> : <div>No pending images</div>}
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
      <Box flexGrow={2} width="300px" height="500px" ml={2}>
        <Typography variant="h5" gutterBottom textAlign="center"> Reference List</Typography>
        <AutoSizer>
          {({ height, width }) => (
            <List
              height={height}
              rowCount={(pendingImages && pendingImages[0].refFilepaths ? pendingImages[0].refFilepaths.length : 1)}
              rowHeight={300}
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
