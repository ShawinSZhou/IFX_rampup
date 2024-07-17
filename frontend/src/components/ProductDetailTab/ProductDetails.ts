import { DemandData } from "../DemandTable/DemandData";
import { ProcessStepData } from "../ProcessStepTable/ProcessStepData";

export interface ProductDetails {
  salesCode: string;
  basicType: string;
  tBase: number;
  parallelity: number;
  chipPerWafer: number;
  reachLevel: number;
  stockBuffer: number;
  ORTLevel: number;
  reworkPercentage: number;
  demandData: DemandData[];
  processStepData: ProcessStepData[];
}
