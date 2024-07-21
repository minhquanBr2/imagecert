interface VerificationResult {
  imageID: string,
  imageURL: string,
  result: number,
  verificationTimestamp: string,
}

interface ColumnData {
  dataKey: keyof VerificationResult;
  label: string;
  numeric?: boolean;
  width: number;
}
