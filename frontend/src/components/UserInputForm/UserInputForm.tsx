import {
  Box,
  Button,
  Stack,
  Grid,
} from "@mui/material";

import { ProductTabsManager } from "../ProductTabsManager/ProductTabsManager";
import { ProductDetailsProvider } from "../ProductDetailContext/ProductDetailContext";

export function UserInputForm() {
  return (
    <Box display="flex" alignItems="center" justifyContent="center">
      <Stack spacing={5}>
        <ProductDetailsProvider>
          <ProductTabsManager />
        </ProductDetailsProvider>

        <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
          <Grid item>
            <Button variant="contained">Generate Excel</Button>
          </Grid>
          <Grid item>
            <Button variant="outlined">Cancel</Button>
          </Grid>
        </Grid>
      </Stack>
    </Box>
  );
}
