import Link from 'next/link';
import { Box, Container, Typography, Button } from '@mui/material';

export default function Home() {
  return (
    <Container maxWidth="md" sx={{ py: 8 }}>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          textAlign: 'center',
          gap: 3,
          minHeight: '60vh',
          justifyContent: 'center',
        }}
      >
        <Typography variant="h2" component="h1" fontWeight={700}>
          Discover Egypt with AI
        </Typography>
        <Typography variant="h6" color="text.secondary" sx={{ maxWidth: 700 }}>
          Identify monuments from photos, ask our smart assistant, and explore Egypt seamlessly.
        </Typography>
        <Button
          component={Link}
          href="/demo"
          variant="contained"
          size="large"
          sx={{ mt: 2 }}
        >
          Try Demo
        </Button>
      </Box>
    </Container>
  );
}