using System;
using System.Linq;
using Microsoft.AspNetCore.Mvc;
using thumbnailService.Context;
using thumbnailService.Converters;
using thumbnailService.Entities.Sql;
using thumbnailService.Models;

namespace thumbnailService.Controllers;

public class JobProcessingApiControllerImpl : JobProcessingApiController
{
    private readonly ModelThumbnailDBContext _context;

    public JobProcessingApiControllerImpl(ModelThumbnailDBContext context) => _context = context;

    public override IActionResult GetQueryJob(Guid id)
    {
        Jobs job = _context.Jobs.SingleOrDefault(i => i.Id.Equals(id));
        JobFullInformation info = job.ToJobFullInformation(_context);
        return new OkObjectResult(info);
    }

    public override IActionResult GetStartJob(Guid id)
    {
        Jobs job = _context.Jobs.SingleOrDefault(i => i.Id.Equals(id));
        job.Statusid = JobStatus.ProcessingEnum.ToGuid(_context);
        _context.Jobs.Update(job);
        _context.SaveChanges();
        
        JobFullInformation info = job.ToJobFullInformation(_context);
        return new OkObjectResult(info);
    }

    public override IActionResult GetThumbnail(Guid id) => throw new NotImplementedException();

    public override IActionResult PostCreateJob(JobDescription jobDescription)
    {
        Jobstatus status = _context.Jobstatus.SingleOrDefault(s => s.Name.Equals(JobStatus.CreatedEnum));
        _context.Jobs.Add(new Jobs(jobDescription.Name, null, null, status));
        return new OkObjectResult(new InlineResponse200());
    }

    public override IActionResult PostSubmitModel(Guid modelID, InlineObject inlineObject) => throw new NotImplementedException();
}
