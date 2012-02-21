{
//=========Macro generated from canvas: c/c
//=========  (Sat Feb 11 18:08:26 2012) by ROOT version5.30/00
   TCanvas *c = new TCanvas("c", "c",0,0,1000,1000);
   c->SetHighLightColor(2);
   c->Range(200,200,2200,2200);
   c->SetFillColor(0);
   c->SetBorderMode(0);
   c->SetBorderSize(2);
   c->SetFrameBorderMode(0);
   c->SetFrameBorderMode(0);
   
   TH2F *exp = new TH2F("exp","",21,400,2000,21,400,2000);
   exp->SetBinContent(528,0.4139077);
   exp->SetEntries(1);
   exp->SetContour(20);
   exp->SetContourLevel(0,0);
   exp->SetContourLevel(1,0);
   exp->SetContourLevel(2,0);
   exp->SetContourLevel(3,0);
   exp->SetContourLevel(4,0);
   exp->SetContourLevel(5,0);
   exp->SetContourLevel(6,0);
   exp->SetContourLevel(7,0);
   exp->SetContourLevel(8,0);
   exp->SetContourLevel(9,0);
   exp->SetContourLevel(10,0);
   exp->SetContourLevel(11,0);
   exp->SetContourLevel(12,0);
   exp->SetContourLevel(13,0);
   exp->SetContourLevel(14,0);
   exp->SetContourLevel(15,0);
   exp->SetContourLevel(16,0);
   exp->SetContourLevel(17,0);
   exp->SetContourLevel(18,0);
   exp->SetContourLevel(19,0);
   
   TPaletteAxis *palette = new TPaletteAxis(2010,400,2100,2000,exp);
palette->SetLabelColor(1);
palette->SetLabelFont(62);
palette->SetLabelOffset(0.005);
palette->SetLabelSize(0.04);
palette->SetTitleOffset(1);
palette->SetTitleSize(0.04);
   palette->SetFillColor(19);
   palette->SetFillStyle(1001);
   exp->GetListOfFunctions()->Add(palette,"br");
   
   TPaveStats *ptstats = new TPaveStats(0.78,0.755,0.98,0.995,"brNDC");
   ptstats->SetName("stats");
   ptstats->SetBorderSize(1);
   ptstats->SetFillColor(0);
   ptstats->SetTextAlign(12);
   TText *text = ptstats->AddText("exp");
   text->SetTextSize(0.0368);
   text = ptstats->AddText("Entries = 1      ");
   text = ptstats->AddText("Mean x =      0");
   text = ptstats->AddText("Mean y =      0");
   text = ptstats->AddText("RMS x =      0");
   text = ptstats->AddText("RMS y =      0");
   ptstats->SetOptStat(1111);
   ptstats->SetOptFit(0);
   ptstats->Draw();
   exp->GetListOfFunctions()->Add(ptstats);
   ptstats->SetParent(exp->GetListOfFunctions());
   exp->GetXaxis()->SetTitle("mSquark / GeV");
   exp->GetYaxis()->SetTitle("mGluino / GeV");
   exp->Draw("COLZ");
   c->Modified();
   c->cd();
   c->SetSelected(c);
}
