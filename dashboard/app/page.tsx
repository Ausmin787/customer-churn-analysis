"use client"

import { useEffect, useState } from "react"
import Papa from "papaparse"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  ChartLegend,
  ChartLegendContent,
  type ChartConfig,
} from "@/components/ui/chart"
import {
  Bar,
  BarChart,
  XAxis,
  YAxis,
  CartesianGrid,
  Line,
  LineChart,
  ReferenceLine,
  Label,
} from "recharts"
import { TrendingDown, Users, Globe, Calendar, Package, Wallet } from "lucide-react"

// ============================================================================
// TYPES
// ============================================================================

type CsvRow = {
  CreditScore: number
  Geography: string
  Gender: string
  Age: number
  Tenure: number
  Balance: number
  NumOfProducts: number
  HasCrCard: number
  IsActiveMember: number
  EstimatedSalary: number
  Exited: number
}

type GeoItem = { country: string; churnRate: number; retentionRate: number }
type AgeGroupItem = { ageGroup: string; churned: number; retained: number }
type ProductItem = { products: string; churnRate: number }
type BalanceData = { churned: number; retained: number }

type ChurnData = {
  overallChurnRate: number
  churnByGeography: GeoItem[]
  avgAgeByCohort: { churned: number; retained: number }
  ageGroupData: AgeGroupItem[]
  churnByProducts: ProductItem[]
  avgBalanceByCohort: BalanceData
}

// ============================================================================
// CHART CONFIGS
// ============================================================================

const geographyChartConfig: ChartConfig = {
  churnRate: { label: "Churn Rate", color: "#ef4444" },
  retentionRate: { label: "Retention Rate", color: "#10b981" },
}

const ageChartConfig: ChartConfig = {
  churned: { label: "Churned", color: "#ef4444" },
  retained: { label: "Retained", color: "#10b981" },
}

const productChartConfig: ChartConfig = {
  churnRate: { label: "Churn Rate", color: "#3b82f6" },
}

// ============================================================================
// HELPERS
// ============================================================================

function round(n: number, decimals: number): number {
  return Math.round(n * Math.pow(10, decimals)) / Math.pow(10, decimals)
}

function computeChurnData(rows: CsvRow[]): ChurnData {
  const total = rows.length
  const churnedRows = rows.filter((r) => r.Exited === 1)
  const retainedRows = rows.filter((r) => r.Exited === 0)

  const overallChurnRate = round((churnedRows.length / total) * 100, 2)

  const churnByGeography: GeoItem[] = ["France", "Germany", "Spain"].map((country) => {
    const g = rows.filter((r) => r.Geography === country)
    const churnRate = round((g.filter((r) => r.Exited === 1).length / g.length) * 100, 2)
    return { country, churnRate, retentionRate: round(100 - churnRate, 2) }
  })

  const avgAgeByCohort = {
    churned: round(churnedRows.reduce((s, r) => s + r.Age, 0) / churnedRows.length, 2),
    retained: round(retainedRows.reduce((s, r) => s + r.Age, 0) / retainedRows.length, 2),
  }

  const ageGroupData: AgeGroupItem[] = [
    { label: "18-30", min: 18, max: 30 },
    { label: "31-40", min: 31, max: 40 },
    { label: "41-50", min: 41, max: 50 },
    { label: "51-60", min: 51, max: 60 },
    { label: "60+", min: 61, max: Infinity },
  ].map(({ label, min, max }) => {
    const g = rows.filter((r) => r.Age >= min && r.Age <= max)
    return {
      ageGroup: label,
      churned: g.filter((r) => r.Exited === 1).length,
      retained: g.filter((r) => r.Exited === 0).length,
    }
  })

  const churnByProducts: ProductItem[] = [1, 2, 3, 4].map((n) => {
    const p = rows.filter((r) => r.NumOfProducts === n)
    return {
      products: String(n),
      churnRate: round((p.filter((r) => r.Exited === 1).length / p.length) * 100, 2),
    }
  })

  const avgBalanceByCohort: BalanceData = {
    churned: round(churnedRows.reduce((s, r) => s + r.Balance, 0) / churnedRows.length, 2),
    retained: round(retainedRows.reduce((s, r) => s + r.Balance, 0) / retainedRows.length, 2),
  }

  return {
    overallChurnRate,
    churnByGeography,
    avgAgeByCohort,
    ageGroupData,
    churnByProducts,
    avgBalanceByCohort,
  }
}

// ============================================================================
// COMPONENTS
// ============================================================================

function KPICard({
  title,
  value,
  label,
  icon: Icon,
  accentColor,
}: {
  title: string
  value: string
  label: string
  icon: React.ElementType
  accentColor: "red" | "orange" | "blue"
}) {
  const colorClasses = {
    red: "text-red-500",
    orange: "text-orange-500",
    blue: "text-blue-500",
  }
  const bgClasses = {
    red: "bg-red-500/10",
    orange: "bg-orange-500/10",
    blue: "bg-blue-500/10",
  }
  return (
    <Card className="border-border/50">
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardDescription className="text-xs sm:text-sm">{title}</CardDescription>
          <div className={`rounded-full p-1.5 sm:p-2 ${bgClasses[accentColor]}`}>
            <Icon className={`h-3 w-3 sm:h-4 sm:w-4 ${colorClasses[accentColor]}`} />
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className={`text-2xl sm:text-3xl font-bold ${colorClasses[accentColor]}`}>{value}</div>
        <p className="text-xs text-muted-foreground mt-1">{label}</p>
      </CardContent>
    </Card>
  )
}

function GeographyChart({ data }: { data: GeoItem[] }) {
  return (
    <Card className="border-border/50 overflow-hidden">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-base sm:text-lg">
          <Globe className="h-4 w-4 sm:h-5 sm:w-5 text-orange-500" />
          Germany Anomaly: Why Is Churn 2x Higher?
        </CardTitle>
        <CardDescription>Churn and retention rates by country</CardDescription>
      </CardHeader>
      <CardContent className="overflow-x-hidden">
        <ChartContainer config={geographyChartConfig} className="h-[250px] sm:h-[300px] w-full">
          <BarChart data={data} barGap={4}>
            <CartesianGrid strokeDasharray="3 3" stroke="#2d3548" vertical={false} />
            <XAxis
              dataKey="country"
              tickLine={false}
              axisLine={false}
              tick={{ fontSize: 11, fill: "#94a3b8" }}
            />
            <YAxis
              tickLine={false}
              axisLine={false}
              tick={{ fontSize: 11, fill: "#94a3b8" }}
              tickFormatter={(value) => `${value}%`}
            />
            <ChartTooltip
              content={<ChartTooltipContent />}
              formatter={(value) => [`${value}%`, ""]}
            />
            <ChartLegend
              content={<ChartLegendContent />}
              wrapperStyle={{ fontSize: "11px" }}
              iconSize={8}
            />
            <Bar dataKey="churnRate" fill="var(--color-churnRate)" radius={[4, 4, 0, 0]} />
            <Bar dataKey="retentionRate" fill="var(--color-retentionRate)" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}

function AgeDistributionChart({ data }: { data: AgeGroupItem[] }) {
  return (
    <Card className="border-border/50 overflow-hidden">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-base sm:text-lg">
          <Calendar className="h-4 w-4 sm:h-5 sm:w-5 text-blue-500" />
          Age Gap: Older Customers Churn More
        </CardTitle>
        <CardDescription>Customer distribution by age group</CardDescription>
      </CardHeader>
      <CardContent className="overflow-x-hidden">
        <ChartContainer config={ageChartConfig} className="h-[250px] sm:h-[300px] w-full">
          <BarChart data={data} barGap={4}>
            <CartesianGrid strokeDasharray="3 3" stroke="#2d3548" vertical={false} />
            <XAxis
              dataKey="ageGroup"
              tickLine={false}
              axisLine={false}
              tick={{ fontSize: 11, fill: "#94a3b8" }}
            />
            <YAxis
              tickLine={false}
              axisLine={false}
              tick={{ fontSize: 11, fill: "#94a3b8" }}
            />
            <ChartTooltip content={<ChartTooltipContent />} />
            <ChartLegend
              content={<ChartLegendContent />}
              wrapperStyle={{ fontSize: "11px" }}
              iconSize={8}
            />
            <Bar dataKey="churned" fill="var(--color-churned)" radius={[4, 4, 0, 0]} />
            <Bar dataKey="retained" fill="var(--color-retained)" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}

function ProductChurnChart({ data }: { data: ProductItem[] }) {
  return (
    <Card className="border-border/50 overflow-hidden">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-base sm:text-lg">
          <Package className="h-4 w-4 sm:h-5 sm:w-5 text-red-500" />
          The Product Trap: More Isn&apos;t Better
        </CardTitle>
        <CardDescription>Churn rate by number of products held</CardDescription>
      </CardHeader>
      <CardContent className="overflow-x-hidden">
        <ChartContainer config={productChartConfig} className="h-[250px] sm:h-[300px] w-full">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#2d3548" vertical={false} />
            <XAxis
              dataKey="products"
              tickLine={false}
              axisLine={false}
              tick={{ fontSize: 11, fill: "#94a3b8" }}
              label={{ value: "Products", position: "bottom", fontSize: 11, fill: "#94a3b8", offset: -5 }}
            />
            <YAxis
              tickLine={false}
              axisLine={false}
              tick={{ fontSize: 11, fill: "#94a3b8" }}
              tickFormatter={(value) => `${value}%`}
              domain={[0, 110]}
            />
            <ChartTooltip
              content={<ChartTooltipContent />}
              formatter={(value) => [`${value}%`, "Churn Rate"]}
            />
            <ReferenceLine y={100} stroke="#ef4444" strokeDasharray="5 5">
              <Label
                value="100% churn"
                position="insideTopRight"
                fill="#ef4444"
                fontSize={11}
              />
            </ReferenceLine>
            <Line
              type="monotone"
              dataKey="churnRate"
              stroke="#3b82f6"
              strokeWidth={3}
              dot={(props: any) => {
                const { cx, cy, payload, index } = props
                const isHighRisk = payload.churnRate >= 80
                return (
                  <circle
                    key={`dot-${index}`}
                    cx={cx}
                    cy={cy}
                    r={isHighRisk ? 8 : 6}
                    fill={isHighRisk ? "#ef4444" : "#3b82f6"}
                    stroke="#1a1f2e"
                    strokeWidth={2}
                  />
                )
              }}
              activeDot={{ r: 8, fill: "#3b82f6" }}
            />
          </LineChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}

function BalanceParadoxCard({ data }: { data: BalanceData }) {
  const difference = data.churned - data.retained
  const percentHigher = ((difference / data.retained) * 100).toFixed(1)

  return (
    <Card className="border-border/50">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-base sm:text-lg">
          <Wallet className="h-4 w-4 sm:h-5 sm:w-5 text-blue-500" />
          The Balance Paradox: Wealthier Customers Leave
        </CardTitle>
        <CardDescription>Higher balance does not mean higher loyalty</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
          <div className="bg-red-500/10 rounded-lg p-4 sm:p-6 border border-red-500/20">
            <div className="text-xs sm:text-sm text-muted-foreground mb-1">Churned Customers</div>
            <div className="text-xl sm:text-2xl font-bold text-red-500">
              €{Math.round(data.churned).toLocaleString()}
            </div>
            <div className="text-xs text-muted-foreground mt-1">Average Balance</div>
          </div>
          <div className="bg-green-500/10 rounded-lg p-4 sm:p-6 border border-green-500/20">
            <div className="text-xs sm:text-sm text-muted-foreground mb-1">Retained Customers</div>
            <div className="text-xl sm:text-2xl font-bold text-green-500">
              €{Math.round(data.retained).toLocaleString()}
            </div>
            <div className="text-xs text-muted-foreground mt-1">Average Balance</div>
          </div>
        </div>
        <div className="mt-4 p-3 sm:p-4 bg-secondary rounded-lg">
          <div className="flex items-center gap-2 text-sm">
            <TrendingDown className="h-4 w-4 text-orange-500" />
            <span className="text-muted-foreground">
              Churned customers have{" "}
              <span className="text-orange-500 font-semibold">{percentHigher}% higher</span>{" "}
              average balance (€{Math.round(difference).toLocaleString()} more)
            </span>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

// ============================================================================
// MAIN PAGE
// ============================================================================

export default function ChurnDashboard() {
  const [data, setData] = useState<ChurnData | null>(null)

  useEffect(() => {
    Papa.parse("/churn_data.csv", {
      download: true,
      header: true,
      dynamicTyping: true,
      skipEmptyLines: true,
      complete: (results) => {
        const rows = results.data as CsvRow[]
        setData(computeChurnData(rows))
      },
    })
  }, [])

  if (!data) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center space-y-2">
          <div className="text-lg font-medium text-foreground">Loading dashboard...</div>
          <div className="text-sm text-muted-foreground">Parsing churn_data.csv</div>
        </div>
      </div>
    )
  }

  const germanyChurnRate = data.churnByGeography.find((g) => g.country === "Germany")?.churnRate ?? 0
  const nonGermanyAvg = round(
    data.churnByGeography
      .filter((g) => g.country !== "Germany")
      .reduce((s, g) => s + g.churnRate, 0) / 2,
    1
  )
  const product4Churn = data.churnByProducts.find((p) => p.products === "4")?.churnRate ?? 100

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border/50 bg-card/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4 sm:py-6">
          <div className="flex items-center gap-3">
            <div className="rounded-lg bg-red-500/10 p-2">
              <Users className="h-5 w-5 sm:h-6 sm:w-6 text-red-500" />
            </div>
            <div>
              <h1 className="text-xl sm:text-2xl font-bold text-foreground">
                Customer Churn Analysis
              </h1>
              <p className="text-xs sm:text-sm text-muted-foreground">
                10,000 bank customers | Key churn drivers identified
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-6 sm:py-8 space-y-6 sm:space-y-8">
        {/* KPI Cards */}
        <section>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
            <KPICard
              title="Overall Churn Rate"
              value={`${data.overallChurnRate}%`}
              label="1 in 5 customers lost"
              icon={TrendingDown}
              accentColor="red"
            />
            <KPICard
              title="Germany Churn Rate"
              value={`${germanyChurnRate}%`}
              label={`vs Global ${nonGermanyAvg}% — 2x the average`}
              icon={Globe}
              accentColor="orange"
            />
            <KPICard
              title="Age Gap"
              value={`${(data.avgAgeByCohort.churned - data.avgAgeByCohort.retained).toFixed(1)} yrs`}
              label={`Churned avg ${data.avgAgeByCohort.churned} vs Retained ${data.avgAgeByCohort.retained}`}
              icon={Calendar}
              accentColor="blue"
            />
            <KPICard
              title="4-Product Trap"
              value={`${product4Churn}%`}
              label="Complete customer loss"
              icon={Package}
              accentColor="red"
            />
          </div>
        </section>

        {/* Geography Chart */}
        <section>
          <GeographyChart data={data.churnByGeography} />
        </section>

        {/* Age Distribution Chart */}
        <section>
          <AgeDistributionChart data={data.ageGroupData} />
        </section>

        {/* Product Churn Chart */}
        <section>
          <ProductChurnChart data={data.churnByProducts} />
        </section>

        {/* Balance Paradox */}
        <section>
          <BalanceParadoxCard data={data.avgBalanceByCohort} />
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-border/50 bg-card/30">
        <div className="container mx-auto px-4 py-4 sm:py-6">
          <p className="text-xs sm:text-sm text-muted-foreground text-center">
            Data: 10,000 bank customers | Analysis: Python, pandas, scikit-learn |{" "}
            <a
              href="https://github.com/Ausmin787"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-500 hover:underline"
            >
              GitHub: Ausmin787
            </a>
          </p>
        </div>
      </footer>
    </div>
  )
}
