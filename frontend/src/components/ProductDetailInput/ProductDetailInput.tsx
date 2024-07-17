import { Box, TextField, Stack, Grid } from "@mui/material";

import { ProductDetailInputProps } from "./ProductDetailInputProps";


export function ProductDetailInput({
  productDetail,
  onInputChange,
  index,
}: ProductDetailInputProps) {
  // 导出一个名为 ProductDetailInput 的功能组件，并解构传递给组件的属性（productDetail, onInputChange, index）
  
  return (
    <Box display="flex" alignItems="center" justifyContent="center">
      <Stack spacing={5}>
        <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
          <Grid item>
            <TextField
              id={`salescode-${index}`}
              label="Salescode"
              value={productDetail.salesCode}
              onChange={(e) => {
                onInputChange("salesCode", e.target.value);
              }}
            ></TextField>
            
            {/* TextField 是一个文本输入字段，它绑定了一个唯一的 ID,显示标签,
            并且它的值被设置为从 productDetail 中读取的 salesCode 属性。
            当输入变化时，会触发 onInputChange 函数，并传递字段名称和新值。 */}
            
          </Grid>
          <Grid item>
            <TextField
              id={`basic-type-${index}`}
              label="Basic type"
              value={productDetail.basicType}
              onChange={(e) => {
                onInputChange("basicType", e.target.value);
              }}
            ></TextField>
          </Grid>
          <Grid item>
            <TextField
              id={`t-base-${index}`}
              label="T BASE"
              value={productDetail.tBase}
              onChange={(e) => {
                onInputChange("tBase", e.target.value);
              }}
            ></TextField>
          </Grid>
        </Grid>

        <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
          <Grid item>
            <TextField
              id={`parallelity-${index}`}
              label="Parallelity"
              value={productDetail.parallelity}
              onChange={(e) => {
                onInputChange("parallelity", e.target.value);
              }}
            ></TextField>
          </Grid>
          <Grid item>
            <TextField
              id={`chip-per-wafer-${index}`}
              label="Chip per wafer"
              value={productDetail.chipPerWafer}
              onChange={(e) => {
                onInputChange("chipPerWafer", Number(e.target.value));
              }}
            ></TextField>
          </Grid>
        </Grid>

        <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
          <Grid item>
            <TextField
              id={`reach-level-${index}`}
              label="Reach level"
              value={productDetail.reachLevel}
              onChange={(e) => {
                onInputChange("reachLevel", Number(e.target.value));
              }}
            ></TextField>
          </Grid>
          <Grid item>
            <TextField
              id={`stock-buffer-${index}`}
              label="Stock buffer"
              value={productDetail.stockBuffer}
              onChange={(e) => {
                onInputChange("stockBuffer", Number(e.target.value));
              }}
            ></TextField>
          </Grid>
          <Grid item>
            <TextField
              id={`ort-level-${index}`}
              label="ORT Level"
              value={productDetail.ORTLevel}
              onChange={(e) => {
                onInputChange("ORTLevel", Number(e.target.value));
              }}
            ></TextField>
          </Grid>
          <Grid item>
            <TextField
              id={`rework-percentage-${index}`}
              label="Rework percentage [%]"
              value={productDetail.reworkPercentage}
              onChange={(e) => {
                onInputChange("reworkPercentage", Number(e.target.value));
              }}
            ></TextField>
          </Grid>
        </Grid>
      </Stack>
    </Box>
  );
}
